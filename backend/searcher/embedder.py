from qdrant_client import QdrantClient, models
from searcher.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME, EMBEDDINGS_MODEL

from tqdm import tqdm
import pandas as pd
import json
import os

from enum import Enum  # Import Enum for creating custom status


class UploadStatus(Enum):
    """
    An enum representing the possible upload statuses.
    """

    SUCCESS = "Upload successful"
    PREPROCESSING_ERROR = "Error preprocessing data"
    QDRANT_ERROR = "Error interacting with Qdrant"
    UNKNOWN_ERROR = "Unknown error during upload"


class DataPreprocessor:
    """
    A class for embedd data from files in JSON and CSV formats.
    """

    def __init__(self, data_dir):
        """
        Initializes the preprocessor with the data directory path.

        Args:
            data_dir (str): The path to the directory containing data files.
        """
        self.data_dir = data_dir

    def preprocess(self, data_file: str):
        """
        Preprocesses a data file and returns extracted documents and metadata.

        Args:
            data_file (str): The name of the data file to process.

        Returns:
            tuple or None:
                - A tuple containing two lists (documents, metadata) if successful.
                - None if there's an error during processing.
        """

        payload_path = os.path.join(self.data_dir, data_file)
        try:
            ext = os.path.splitext(data_file)[1].lower()

            if ext == ".json":
                return self._process_json(payload_path)

            elif ext == ".csv":
                return self._process_csv(payload_path)

            else:
                return None  # Handle unsupported file formats gracefully

        except (FileNotFoundError, json.JSONDecodeError, pd.errors.ParserError) as e:
            # Handle potential errors during processing
            print(f"Error processing data file '{data_file}': {e}")
            return None

    def _process_json(self, payload_path: str):
        """Processes a JSON file, extracting documents and metadata."""

        documents, metadata = [], []
        with open(payload_path, "r") as fd:
            for line in fd:
                obj = json.loads(line)
                documents.append(obj.pop("description", ""))
                metadata.append({
                    "logo_url": obj.pop("images", ""),
                    "homepage_url": obj.pop("link", ""),
                    **obj
                })
        return documents, metadata

    def _process_csv(self, payload_path: str):
        """Processes a CSV file, extracting documents and metadata."""

        df = pd.read_csv(payload_path)
        documents = df['short_description'].tolist()
        metadata = df.drop(columns=['short_description']).to_dict('records')
        return documents, metadata

    
class Uploader:
    """
    A class for uploading preprocessed data with embeddings to a Qdrant collection.
    """

    def __init__(self, data_dir: str = DATA_DIR, qdrant_url: str = QDRANT_URL, qdrant_api_key: str = QDRANT_API_KEY, embeddings_model: str = EMBEDDINGS_MODEL, collection_name: str = COLLECTION_NAME, text_field_name: str = TEXT_FIELD_NAME) -> None:
        """
        Initializes the uploader with various configurations.

        Args:
            data_dir (str): The path to the directory containing data files.
            qdrant_url (str): The URL of the Qdrant server.
            qdrant_api_key (str): The API key for Qdrant authentication.
            embeddings_model (str): The name of the embeddings model used for document representation.
            collection_name (str): The name of the Qdrant collection to upload data to.
            text_field_name (str): The name of the field in metadata containing text for indexing.
        """

        self.data_dir = data_dir
        self.qdrant_url = qdrant_url
        self.qdrant_api_key = qdrant_api_key
        self.embeddings_model = embeddings_model
        self.collection_name = collection_name
        self.text_field_name = text_field_name

        self.client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            prefer_grpc=True,
        )

    def upload_embeddings(self, data_file: str) -> UploadStatus:
        """
        Uploads preprocessed documents and metadata with embeddings to Qdrant.

        Args:
            data_file (str): The name of the data file to process and upload.

        Returns:
            UploadStatus: An enum value indicating the upload status.
        """
        try:
            # Preprocess data using the separate DataPreprocessor class
            documents, metadata = DataPreprocessor(self.data_dir).preprocess(data_file)

            self.client.set_model(self.embeddings_model)

            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=self.client.get_fastembed_vector_params(on_disk=True),
                quantization_config=models.ScalarQuantization(
                    scalar=models.ScalarQuantizationConfig(
                        type=models.ScalarType.INT8,
                        quantile=0.99,
                        always_ram=True
                    )
                )
            )

            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name=self.text_field_name,
                field_schema=models.TextIndexParams(
                    type=models.TextIndexType.TEXT,
                    tokenizer=models.TokenizerType.WORD,
                    min_token_len=2,
                    max_token_len=20,
                    lowercase=True,
                )
            )

            self.client.add(
                collection_name=self.collection_name,
                documents=documents,
                metadata=metadata,
                ids=tqdm(range(len(documents))),
                parallel=0,
            )

            return UploadStatus.SUCCESS
        
        except Exception as e:
            print(f"Error uploading data to Qdrant: {e}")
            return UploadStatus.UNKNOWN_ERROR