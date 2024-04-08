# Searcher

Neural search and text search with Qdrant vectorDB, sentence-transformers embedding models, and FastAPI.

The demo is based on the vector search engine Qdrant and [demo app](https://github.com/qdrant/qdrant_demo).

## Requirements
python:
```
pip install poetry
poetry install
```

as well as docker and docker compose.

## Upload data to searcher
### startups dataset
o launch this demo locally you will need to download data first.

The source of the original data is https://www.startups-list.com/

Download the data via the following command:
```
wget https://storage.googleapis.com/generall-shared-data/startups_demo.json -P data/
```
To launch the service, use
```
docker-compose up -d
```
After service is started you can upload initial data to the search engine.
```
cd Searcher/backend 
python -m searcher.init_collection_startup
```

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
