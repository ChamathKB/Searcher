from sentence_transformers.cross_encoder import CrossEncoder

from .neural_searcher import NeuralSearcher
from .text_searcher import TextSearcher
from .config import CROSSENCODER_MODEL

# resolve dependancies
model = CrossEncoder(CROSSENCODER_MODEL)

class HybridSearcher:
    def __init__(self, collection_name: str):
        self.text_searcher = TextSearcher(collection_name)
        self.neural_searcher = NeuralSearcher(collection_name)

    def search(self, query: str):
        keyword_results = self.text_searcher(query)
        neural_results = self.neural_searcher(query)
        all_results = keyword_results + neural_results
        ranks = model.rank(query, all_results)
        return ranks
