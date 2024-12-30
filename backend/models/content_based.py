

# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import linear_kernel


# class ContentBasedModel:
#     def __init__(self, movies):
#         """
#         Initialize the content-based model with movie data.
#         """
#         self.movies = movies
#         self.genre_matrix = self._vectorize_genres()

#     def _vectorize_genres(self):
#         """
#         Vectorize genres for similarity computation.
#         """
#         count_vectorizer = CountVectorizer()
#         return count_vectorizer.fit_transform(self.movies["genres"])

#     def recommend(self, movie_title, n=5):
#         """
#         Recommend top N movies based on content similarity.
#         """
#         if movie_title not in self.movies["title"].values:
#             return []

#         idx = self.movies[self.movies["title"] == movie_title].index[0]
#         similarity_scores = linear_kernel(self.genre_matrix[idx], self.genre_matrix).flatten()
#         similar_indices = similarity_scores.argsort()[-n - 1 : -1][::-1]
#         recommendations = self.movies.iloc[similar_indices][["title"]]
#         return recommendations.to_dict("records")


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedModel:
    def __init__(self, movies):
        self.movies = movies
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.genre_matrix = self.vectorizer.fit_transform(self.movies["genres"])

    def recommend(self, movie_title, n=5):
        if movie_title not in self.movies["title"].values:
            return []

        idx = self.movies[self.movies["title"] == movie_title].index[0]
        cosine_similarities = cosine_similarity(self.genre_matrix[idx], self.genre_matrix).flatten()
        similar_indices = cosine_similarities.argsort()[-n - 1 : -1][::-1]
        recommendations = self.movies.iloc[similar_indices]["title"].tolist()
        return recommendations
