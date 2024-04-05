from flashrank import Ranker, RerankRequest
from typing import List, Dict

from .neural_searcher import NeuralSearcher
from .text_searcher import TextSearcher

ranker = Ranker()

class HybridSearcher:
    def __init__(self, collection_name: str):
        self.text_searcher = TextSearcher(collection_name)
        self.neural_searcher = NeuralSearcher(collection_name)
        
    def convert_data(data):
        """Converts a list of dictionaries to a list of dictionaries with desired format.

        Args:
            data: A list of dictionaries containing information about documents.

        Returns:
            A list of dictionaries with "id", "text", and "meta" fields.
        """
        converted_data = []
        for i, item in enumerate(data):
            converted_data.append({
                "id": i + 1,
                "text": item["document"],
                "meta": {"additional": f"info{i + 1}"}
            })
        return converted_data

    def search(self, query: str) -> List[Dict]:
        """Performs a hybrid search using keyword and neural search, followed by reranking.

        This function combines the results from keyword search and neural search for a given query.
        It then reranks the combined results using the provided ranker before returning them.

        Args:
            query (str): The search query string.

        Returns:
            List[Dict]: A list of dictionaries representing the top search results,
                        formatted similar to the output of `search` and `highlight` functions.
                        Each dictionary includes "id", "text", "meta", and potentially a "score" field.
        """
        keyword_results = self.text_searcher.search(query)
        neural_results = self.neural_searcher.search(query)
        all_results = keyword_results + neural_results
        converted_data = HybridSearcher.convert_data(all_results)
        reranked_results = RerankRequest(query=query, passages=converted_data)
        results = ranker.rerank(reranked_results)
        # return [{"id": result["id"], "text": result["text"], "meta": result.get("meta", {}), "score": result.get("score", 0.0)} for result in reranked_results]
        print(results)
        return results
