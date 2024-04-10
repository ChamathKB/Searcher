# Searcher

Neural search and text as well as hybrid search with Qdrant vectorDB, sentence-transformers embedding models, cross-encoder models, and FastAPI.

The demo is based on the vector search engine Qdrant and [demo app](https://github.com/qdrant/qdrant_demo) but offers a more tailored implementation for hybrid search.

## Requirements
python:
```
pip install poetry
poetry install
```

as well as docker and docker compose.

## Usage
### 1. Download Startup Dataset:
The source of the original data is https://www.startups-list.com/

Download the data via the following command:
```
wget https://storage.googleapis.com/generall-shared-data/startups_demo.json -P data/
```

### 2. Launch using Docker:

Use Docker Compose to launch the service in containers:
```
docker-compose up -d
```

### 3. Uploading Data (Two Options):
After service is started you can upload initial data to the search engine.

#### Option A: Initial Upload via Script:
```
cd Searcher/backend 
python -m searcher.init_collection_startup
```

#### Option B: Upload via API:

Ensure the service is running (either locally or in containers) and use a tool like Postman or curl to send a POST request to http://localhost:8000/api/upload with the data file included in the request body. For example, with curl:
```
curl -X POST http://localhost:8000/api/upload -F "file=@startups_demo.json"
```
Additional Notes:

Replace http://localhost:8000 with the appropriate URL if you're accessing the API from a different machine.

# Search API
In the API, there are three distinct search methods available:
1. Neural
2. Text
3. Hybrid

## 1. Neural Search
Neural Search utilizes embeddings models to perform vector search operations on the vectorDB.

To execute a Neural Search, use the following cURL command:
```
curl -X GET "http://localhost:8000/api/search?q=QTECT&search_type=neural"
```

## 2. Text Search
Text Search employs the MatchText filter to match text within documents against the provided query.

To initiate a Text Search, use the following cURL command:
```
curl -X GET "http://localhost:8000/api/search?q=QTECT&search_type=text"
```

## 3. Hybrid Search
Hybrid Search combines both Neural Search and Text Search methodologies, subsequently re-ranking the results using cross-encoder models. This approach ensures the retrieval of the most accurate results in specific scenarios.

For more detailed information on Hybrid Search, visit the following link: [Hybrid Search Article](https://qdrant.tech/articles/hybrid-search/)

To perform a Hybrid Search, utilize the following cURL command:
```
curl -X GET "http://localhost:8000/api/search?q=QTECT&search_type=hybrid"
```
