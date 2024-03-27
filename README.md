# Searcher

Neural search and text search with Qdrant vectorDB, sentence-transformers embedding models, and FastAPI.

The demo is based on the vector search engine Qdrant.

## Requirements
python:
```
pip install poetry
poetry install
```

as well as docker and docker compose

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

