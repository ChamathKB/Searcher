from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchText
from typing import List, Dict
import re

from .config import QDRANT_URL, QDRANT_API_KEY, TEXT_FIELD_NAME


class TextSearcher:
    def __init__(self, collection_name: str):
        self.highlight_field = TEXT_FIELD_NAME
        self.collection_name = collection_name
        self.qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=True)

    def highlight(self, record: Dict, query: str) -> Dict:
        """ Highlights the query in the text field.

        Args:
            record: A dictionary representing a document.
            query: The search query string.

        Returns:
            The document dictionary with the highlighted text field.
        """
        text = record[self.highlight_field]

        for word in query.lower().split():
            if len(word) > 4:
                pattern = re.compile(fr"(\b{re.escape(word)}?.?\b)", flags=re.IGNORECASE)
            else:
                pattern = re.compile(fr"(\b{re.escape(word)}\b)", flags=re.IGNORECASE)
            text = re.sub(pattern, r"<b>\1</b>", text)

        record[self.highlight_field] = text
        return record


    def search(self, query: str, top: int=5) -> List[Dict]:
        """ Searches for documents containing the query.

        Args:
            query (str): The search query string.
            top (int, optional): The maximum number of documents to return. Defaults to 5.

        Returns:
            List[Dict]: A list of highlighted documents (dictionaries).
        """
        hits = self.qdrant_client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key=TEXT_FIELD_NAME,
                        match=MatchText(text=query),
                    )
                ]),
            with_payload=True,
            with_vectors=False,
            limit=top
        )
        return [self.highlight(hit.payload, query) for hit in hits[0]]