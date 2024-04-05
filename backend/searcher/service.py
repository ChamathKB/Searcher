from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .config import COLLECTION_NAME, STATIC_DIR
from .neural_searcher import NeuralSearcher
from .text_searcher import TextSearcher
from .hybrid_searcher import HybridSearcher

from typing import Optional
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
        results = hybrid_searcher.search(query=q)  # Use hybrid search function
        print("hybrid")
    elif search_type=="neural":
        results = neural_searcher.search(text=q)  # Use neural search if requested
        print("neural")
    else:
        results = text_searcher.search(query=q)  # Default to text search
        print("text")

    return {"result": results}

if os.path.exists(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
