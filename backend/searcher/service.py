from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .config import COLLECTION_NAME, STATIC_DIR, DATA_DIR
from .neural_searcher import NeuralSearcher
from .text_searcher import TextSearcher
from .hybrid_searcher import HybridSearcher
from .embedder import Uploader, UploadStatus

from typing import Dict
import uvicorn
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

neural_searcher = NeuralSearcher(collection_name=COLLECTION_NAME)
text_searcher = TextSearcher(collection_name=COLLECTION_NAME)
hybrid_searcher = HybridSearcher(collection_name=COLLECTION_NAME)


@app.get("/api/search")
async def read_item(q: str, search_type: str = "hybrid") -> Dict:
    """
    Performs a search based on the provided query and search type.

    This endpoint supports three search types:

    - Text search (default): Uses the text search engine for efficient keyword-based search.
    - Neural search (optional, requires `neural=True`): Uses the neural search engine for more semantic understanding.
    - Hybrid search (optional, requires `hybrid=True`): Combines text and neural search results, followed by reranking.

    Args:
        q (str): The search query string.
        neural (bool, optional): Whether to perform neural search (defaults to True).
        hybrid (bool, optional): Whether to perform hybrid search (defaults to False).

    Returns:
        Dict: A dictionary containing the search results in the format expected by the client.
              The exact format may depend on the chosen search type (text, neural, or hybrid).
    """

    if search_type=="hybrid":
        results = hybrid_searcher.search(query=q)  
    elif search_type=="neural":
        results = neural_searcher.search(text=q)  
    else:
        results = text_searcher.search(query=q)  

    return {"result": results}


@app.post("/api/upload")
async def upload_embeddings(file: UploadFile = File(...)) -> Dict:
    """
    Uploads preprocessed data with embeddings to a Qdrant collection.

    Args:
        file (UploadFile): The uploaded file containing data.

    Returns:
        dict: A dictionary containing the upload status message.
    """

    filename = file.filename
    content = await file.read()

    # Save the uploaded file temporarily
    with open(os.path.join(DATA_DIR, filename), "wb") as buffer:
        buffer.write(content)

    uploader = Uploader()

    status = uploader.upload_embeddings(filename)

    # Remove the temporary file
    os.remove(os.path.join(DATA_DIR, filename))

    if status == UploadStatus.SUCCESS:
        return {"message": "Embeddings uploaded successfully!"}
    else:
        return {"message": f"Upload failed: {status.value}"}


if os.path.exists(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
