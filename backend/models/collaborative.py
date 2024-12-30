from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import pandas as pd

class CollaborativeModel:
    def __init__(self, ratings, movies):
        """
        Initialize the Collaborative Filtering model with ratings and movies data.
        :param ratings: DataFrame containing user ratings.
        :param movies: DataFrame containing movie metadata.
        """
        self.ratings = ratings
        self.movies = movies
        self.model = None

    def train_model(self):
        """
        Train the collaborative filtering model using Surprise SVD.
        Returns the test set for evaluation.
        """
        reader = Reader(rating_scale=(0.5, 5.0))
        data = Dataset.load_from_df(self.ratings[["userId", "movieId", "rating"]], reader)
        
        # Split the data into training and test sets
        trainset, testset = train_test_split(data, test_size=0.2)

        # Initialize and train the SVD model
        self.model = SVD()
        self.model.fit(trainset)

        return testset

    def recommend(self, user_id=None, n=5):
        """
        Recommend top N movies for a user. If no user_id is provided, recommend top-rated movies across all users.
        :param user_id: ID of the user.
        :param n: Number of recommendations.
        :return: List of recommended movies with metadata.
        """
        if user_id is not None:
            # Personalized recommendations for a specific user
            all_movie_ids = self.ratings["movieId"].unique()
            watched_movie_ids = self.ratings[self.ratings["userId"] == user_id]["movieId"].tolist()

            recommendations = [
                (movie_id, self.model.predict(user_id, movie_id).est)
                for movie_id in all_movie_ids
                if movie_id not in watched_movie_ids
            ]
            recommendations.sort(key=lambda x: x[1], reverse=True)
            top_recommendations = recommendations[:n]

            # Fetch movie titles and metadata for the recommendations
            recommended_movies = self.movies[self.movies["movieId"].isin([rec[0] for rec in top_recommendations])]
        else:
            # Global recommendations based on average ratings
            avg_ratings = self.ratings.groupby("movieId")["rating"].mean().sort_values(ascending=False)
            top_movie_ids = avg_ratings.head(n).index.tolist()
            recommended_movies = self.movies[self.movies["movieId"].isin(top_movie_ids)]

        # Format the recommendations with movie metadata
        recommendations = [
            {
                "title": row["title"],
                "genres": row["genres"],
                "movieId": row["movieId"]
            }
            for _, row in recommended_movies.iterrows()
        ]

        return recommendations
