from qdrant_client import QdrantClient, models
from searcher.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME, EMBEDDINGS_MODEL

from tqdm import tqdm
import pandas as pd
import json
import os


def preprocessor(data_file):

    payload_path = os.path.join(DATA_DIR, data_file)
    if data_file.endswith(".json"):
        metadata = []
        documents = []
	    
        with open(payload_path, "r") as fd:
            for line in fd:
                obj = json.loads(line)
                documents.append(obj.pop("description"))
                obj["logo_url"] = obj.pop("images")
                obj["homepage_url"] = obj.pop("link")
                metadata.append(obj)
        return documents, metadata
	      
    elif data_file.endswith(".csv"):
        df = pd.read_csv(payload_path)
        documents = df['short_description'].tolist()
        df.drop(columns=['short_description'], inplace=True)
        metadata = df.to_dict('records')
        return documents, metadata
    else:
     	return None


    
def upload_embeddings(data_file):
    documents, metadata = preprocessor(data_file)
    
    client = QdrantClient(
        url=QDRANT_URL, 
        api_key=QDRANT_API_KEY,
        prefer_grpc=True,
        )

    client.set_model(EMBEDDINGS_MODEL)

    
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=client.get_fastembed_vector_params(on_disk=True),
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                quantile=0.99,
                always_ram=True
            )
        )
    )

    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name=TEXT_FIELD_NAME,
        field_schema=models.TextIndexParams(
            type=models.TextIndexType.TEXT,
            tokenizer=models.TokenizerType.WORD,
            min_token_len=2,
            max_token_len=20,
            lowercase=True,
        )
    )

    client.add(
        collection_name=COLLECTION_NAME,
        documents=documents,
        metadata=metadata,
        ids=tqdm(range(len(documents))),
        parallel=0,
    )

