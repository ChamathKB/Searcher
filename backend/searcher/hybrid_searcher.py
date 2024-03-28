from .neural_searcher import NeuralSearcher
from .text_searcher import TextSearcher

class HybridSearcher:
    def __init__(self, collection_name: str, query: str):
        # self.text_searcher = TextSearcher(collection_name, query)
        # self.neural_searcher = NeuralSearcher(collection_name, query)
        self.collection_name = collection_name
        self.query = query

    async def search(self, query):
        # TODO
        # re-ranking https://qdrant.tech/articles/hybrid-search/
        key_word_result = await TextSearcher(self.collection_name, query).search()

        if len(key_word_result) > 3:
            return key_word_result
        else:
            neural_search = await NeuralSearcher(self.collection_name, query).search()
            return neural_search