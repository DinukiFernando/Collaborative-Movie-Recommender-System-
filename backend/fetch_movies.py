# import requests
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import linear_kernel
# from surprise import Dataset, Reader, SVD
# from surprise.model_selection import train_test_split
# import pandas as pd

# OMDB_API_KEY = "d0ba67d6"  # Replace with your OMDB API key

# # Load Movie Metadata
# movies = pd.read_csv("ml-latest-small/ml-latest-small/movies.csv")
# ratings = pd.read_csv("ml-latest-small/ml-latest-small/ratings.csv")
# movies["genres"] = movies["genres"].str.replace("|", " ", regex=False)

# # Vectorize Genres
# count_vectorizer = CountVectorizer()
# genre_matrix = count_vectorizer.fit_transform(movies["genres"])


# def fetch_poster(movie_title):
#     """Fetch movie poster from OMDB API."""
#     url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie_title}"
#     response = requests.get(url)
#     print(f"Fetching poster for {movie_title}: {response.json()}")  # Debugging log
#     if response.status_code == 200:
#         data = response.json()
#         poster = data.get("Poster", "")
#         if poster == "N/A":  # Handle missing posters
#             return "https://via.placeholder.com/300x450?text=No+Image"
#         return poster
#     return "https://via.placeholder.com/300x450?text=No+Image"




# def recommend_by_content(movie_title, n=5):
#     """Recommend movies based on content (genres)."""
#     if movie_title not in movies["title"].values:
#         return {"Error": "Movie not found"}

#     idx = movies[movies["title"] == movie_title].index[0]
#     similarity_scores = linear_kernel(genre_matrix[idx], genre_matrix).flatten()
#     similar_indices = similarity_scores.argsort()[-n-1:-1][::-1]
#     recommended_movies = movies.iloc[similar_indices]["title"].tolist()

#     # Fetch poster URLs for the recommended movies
#     recommendations = [
#         {"title": movie, "poster": fetch_poster(movie)} for movie in recommended_movies
#     ]
#     return recommendations


# # Set up Surprise for collaborative filtering
# reader = Reader(rating_scale=(0.5, 5.0))
# data = Dataset.load_from_df(ratings[["userId", "movieId", "rating"]], reader)
# trainset, testset = train_test_split(data, test_size=0.2)
# model = SVD()
# model.fit(trainset)


# def recommend_by_collaborative(user_id, n=5):
#     """Recommend movies based on collaborative filtering."""
#     user_ratings = ratings[ratings["userId"] == user_id]
#     watched_movies = user_ratings["movieId"].tolist()

#     all_movie_ids = ratings["movieId"].unique()
#     recommendations = [
#         (movie_id, model.predict(user_id, movie_id).est)
#         for movie_id in all_movie_ids
#         if movie_id not in watched_movies
#     ]
#     recommendations.sort(key=lambda x: x[1], reverse=True)
#     top_recommendations = recommendations[:n]

#     recommended_titles = movies[movies["movieId"].isin([rec[0] for rec in top_recommendations])][
#         "title"
#     ].tolist()
#     recommendations = [
#         {"title": title, "poster": fetch_poster(title)} for title in recommended_titles
#     ]
#     return recommendations


# def hybrid_recommendation(user_id, movie_title, n=5):
#     """Combine content-based and collaborative filtering."""
#     content_recs = recommend_by_content(movie_title, n=n * 2)
#     collaborative_recs = recommend_by_collaborative(user_id, n=n * 2)

#     combined_recommendations = {rec["title"]: rec for rec in content_recs + collaborative_recs}
#     hybrid_recs = list(combined_recommendations.values())[:n]
#     return hybrid_recs


import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import pandas as pd

OMDB_API_KEY = "d0ba67d6"  # Replace with your OMDB API key

# Load Movie Metadata
movies = pd.read_csv("ml-latest-small/ml-latest-small/movies.csv")
ratings = pd.read_csv("ml-latest-small/ml-latest-small/ratings.csv")
movies["genres"] = movies["genres"].str.replace("|", " ", regex=False)

# Vectorize Genres
count_vectorizer = CountVectorizer()
genre_matrix = count_vectorizer.fit_transform(movies["genres"])


def fetch_poster(movie_title):
    """Fetch movie poster from OMDB API."""
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie_title}"
    response = requests.get(url)
    print(f"Fetching poster for {movie_title}: {response.json()}")  # Debugging log
    if response.status_code == 200:
        data = response.json()
        poster = data.get("Poster", "")
        if poster == "N/A":  # Handle missing posters
            return "https://via.placeholder.com/300x450?text=No+Image"
        return poster
    return "https://via.placeholder.com/300x450?text=No+Image"


def recommend_by_content(movie_title, n=5):
    """Recommend movies based on content (genres)."""
    if movie_title not in movies["title"].values:
        return {"Error": "Movie not found"}

    idx = movies[movies["title"] == movie_title].index[0]
    similarity_scores = linear_kernel(genre_matrix[idx], genre_matrix).flatten()
    similar_indices = similarity_scores.argsort()[-n - 1 : -1][::-1]
    recommended_movies = movies.iloc[similar_indices]["title"].tolist()

    # Fetch poster URLs for the recommended movies
    recommendations = [
        {"title": movie, "poster": fetch_poster(movie)} for movie in recommended_movies
    ]
    return recommendations


# Set up Surprise for collaborative filtering
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings[["userId", "movieId", "rating"]], reader)
trainset, testset = train_test_split(data, test_size=0.2)
model = SVD()
model.fit(trainset)


def recommend_by_collaborative_all_users(n=5):
    """Recommend movies based on collaborative filtering across all users."""
    # Calculate the average rating for each movie
    movie_ratings = ratings.groupby("movieId")["rating"].mean()
    
    # Sort movies by their average rating in descending order
    top_movie_ids = movie_ratings.sort_values(ascending=False).head(n).index.tolist()
    
    # Get the titles of the top movies
    recommended_titles = movies[movies["movieId"].isin(top_movie_ids)]["title"].tolist()
    
    # Fetch posters for the top recommended movies
    recommendations = [
        {"title": title, "poster": fetch_poster(title)} for title in recommended_titles
    ]
    return recommendations


def hybrid_recommendation_all_users(movie_title, n=5):
    """Combine content-based filtering with collaborative filtering for all users."""
    # Get content-based recommendations
    content_recs = recommend_by_content(movie_title, n=n * 2)

    # Get collaborative recommendations for all users
    collaborative_recs = recommend_by_collaborative_all_users(n=n * 2)

    # Combine and rank recommendations
    combined_recommendations = {rec["title"]: rec for rec in content_recs + collaborative_recs}
    hybrid_recs = list(combined_recommendations.values())[:n]
    return hybrid_recs
