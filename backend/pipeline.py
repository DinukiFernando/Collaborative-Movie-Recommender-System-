

from preprocessing.load_data import load_data
from models.content_based import ContentBasedModel
from models.collaborative import CollaborativeModel
from models.hybrid import HybridModel
from evaluation import evaluate_content_model, evaluate_collaborative_model


def generate_ground_truth(movie_title, movies, n=5):
    """
    Generate ground truth dynamically based on similar genres.
    :param movie_title: The input movie title.
    :param movies: The movies DataFrame.
    :param n: Number of ground truth items to generate.
    :return: List of movie titles as ground truth.
    """
    if movie_title not in movies["title"].values:
        return []

    input_genres = movies[movies["title"] == movie_title]["genres"].values[0]
    similar_movies = movies[movies["genres"] == input_genres]
    ground_truth = similar_movies["title"].tolist()

    # Exclude the input movie and return top N
    ground_truth = [title for title in ground_truth if title != movie_title][:n]
    return ground_truth


def run_pipeline(ratings_path, movies_path):
    """
    Load data, initialize models, train, and evaluate them.
    """
    # Load datasets
    ratings, movies = load_data(ratings_path, movies_path)

    # Initialize models
    content_model = ContentBasedModel(movies)
    collaborative_model = CollaborativeModel(ratings, movies)
    hybrid_model = HybridModel(content_model, collaborative_model)

    # Train the collaborative model
    testset = collaborative_model.train_model()

    # Evaluate collaborative model
    collaborative_metrics = evaluate_collaborative_model(collaborative_model, testset)
    print("Collaborative Filtering Evaluation:", collaborative_metrics)

    # Evaluate content-based model
    movie_title = "Toy Story (1995)"  # Example input movie title
    content_recommendations = content_model.recommend(movie_title, n=10)
    ground_truth = generate_ground_truth(movie_title, movies, n=10)

    print("Content Recommendations:", content_recommendations)
    print("Ground Truth:", ground_truth)

    precision, recall = evaluate_content_model(content_recommendations, ground_truth)
    print("Content-Based Filtering Evaluation:")
    print(f"Precision: {precision}, Recall: {recall}")

    # Movie titles for autocomplete
    movie_titles = movies["title"].tolist()

    return {
        "content_model": content_model,
        "collaborative_model": collaborative_model,
        "hybrid_model": hybrid_model,
        "movie_titles": movie_titles,
        "evaluation": {
            "collaborative": collaborative_metrics,
            "content": {"precision": precision, "recall": recall},
        },
    }


# from preprocessing.load_data import load_data
# from models.content_based import ContentBasedModel
# from models.collaborative import CollaborativeModel
# from models.hybrid import HybridModel
# from evaluation import evaluate_content_model, evaluate_collaborative_model


# def run_pipeline(ratings_path, movies_path):
#     """
#     Load data, initialize models, train, and evaluate them.
#     """
#     # Load datasets
#     ratings, movies = load_data(ratings_path, movies_path)

#     # Initialize models
#     content_model = ContentBasedModel(movies)
#     collaborative_model = CollaborativeModel(ratings, movies)
#     hybrid_model = HybridModel(content_model, collaborative_model)

#     # Train collaborative model
#     testset = collaborative_model.train_model()

#     # Evaluate models
#     collaborative_metrics = evaluate_collaborative_model(collaborative_model, testset)
#     print("Collaborative Filtering Evaluation:", collaborative_metrics)

#     # Evaluate content-based model
#     movie_title = "Toy Story (1995)"
#     ground_truth = ["A Bug's Life (1998)", "Monsters, Inc. (2001)"]
#     content_recommendations = content_model.recommend(movie_title, n=5)
#     precision, recall = evaluate_content_model(content_recommendations, ground_truth)
#     print("Content-Based Filtering Evaluation:")
#     print(f"Precision: {precision}, Recall: {recall}")

#     # Movie titles for autocomplete
#     movie_titles = movies["title"].tolist()

#     return {
#         "content_model": content_model,
#         "collaborative_model": collaborative_model,
#         "hybrid_model": hybrid_model,
#         "movie_titles": movie_titles,
#         "evaluation": {
#             "collaborative": collaborative_metrics,
#             "content": {"precision": precision, "recall": recall},
#         },
#     }
