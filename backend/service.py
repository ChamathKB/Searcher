from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .config import COLLECTION_NAME, STATIC_DIR
from .neural_searcher import NeuralSearcher
from .text_searcher import TextSearcher

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


@app.get("/api/search")
async def read_item(q: str, neural: bool = True):
    return {
        "result": neural_searcher.search(text=q)
        if neural else text_searcher.search(query=q)
    }


# Mount the static files directory once the search endpoint is defined
if os.path.exists(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
