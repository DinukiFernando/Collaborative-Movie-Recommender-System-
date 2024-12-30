class HybridModel:
    def __init__(self, content_model, collaborative_model):
        self.content_model = content_model
        self.collaborative_model = collaborative_model

    def recommend(self, movie_title, n=5):
        content_recs = self.content_model.recommend(movie_title, n=n * 2)
        collaborative_recs = self.collaborative_model.recommend(n=n * 2)

        combined = {rec["title"]: rec for rec in content_recs + collaborative_recs}
        return list(combined.values())[:n]
