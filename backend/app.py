from flask import Flask, request, jsonify
from flask_cors import CORS
from fetch_movies import (
    recommend_by_content,
    recommend_by_collaborative_all_users,
    hybrid_recommendation_all_users,
    movies,
)

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests


@app.route('/api/content', methods=['GET'])
def content_recommend():
    """Provide content-based recommendations."""
    movie_title = request.args.get('title')
    if not movie_title:
        return jsonify({"error": "Please provide a movie title"}), 400

    recommendations = recommend_by_content(movie_title)
    return jsonify({"recommendations": recommendations})


@app.route('/api/collaborative', methods=['GET'])
def collaborative_recommend():
    """Provide collaborative recommendations based on all users."""
    try:
        recommendations = recommend_by_collaborative_all_users(n=10)  # Adjust the number as needed
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/movies', methods=['GET'])
def get_movies():
    """Return all movie names for autocomplete."""
    try:
        movie_names = movies["title"].tolist()
        return jsonify(movie_names)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/hybrid', methods=['GET'])
def hybrid_recommend():
    """Provide hybrid recommendations."""
    movie_title = request.args.get('title')
    if not movie_title:
        return jsonify({"error": "Please provide a movie title"}), 400

    try:
        recommendations = hybrid_recommendation_all_users(movie_title, n=10)  # Adjust the number as needed
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from pipeline import run_pipeline
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# CORS(app)



# # Load pipeline data
# pipeline_data = run_pipeline("ml-latest-small/ml-latest-small/ratings.csv", "ml-latest-small/ml-latest-small/movies.csv")


# @app.route('/api/content', methods=['GET'])
# def content_recommend():
#     """Content-based recommendations."""
#     movie_title = request.args.get('title')
#     if not movie_title:
#         return jsonify({"error": "Please provide a movie title"}), 400
#     recommendations = pipeline_data["content_model"].recommend(movie_title)
#     return jsonify({"recommendations": recommendations})


# @app.route('/api/collaborative', methods=['GET'])
# def collaborative_recommend():
#     """Collaborative recommendations."""
#     recommendations = pipeline_data["collaborative_model"].recommend()
#     return jsonify({"recommendations": recommendations})


# @app.route('/api/movies', methods=['GET'])
# def get_movies():
#     """Movie names for autocomplete."""
#     movie_names = pipeline_data["movie_titles"]
#     return jsonify(movie_names)


# @app.route('/api/hybrid', methods=['GET'])
# def hybrid_recommend():
#     """Hybrid recommendations."""
#     movie_title = request.args.get('title')
#     if not movie_title:
#         return jsonify({"error": "Please provide a movie title"}), 400
#     recommendations = pipeline_data["hybrid_model"].recommend(movie_title)
#     return jsonify({"recommendations": recommendations})

# @app.route('/api/evaluate', methods=['GET'])
# def evaluate():
#     """API endpoint to evaluate models."""
#     results = run_pipeline("ml-latest-small/ratings.csv", "ml-latest-small/movies.csv")
#     return jsonify(results)

# if __name__ == "__main__":
#     app.run(debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from pipeline import run_pipeline

# app = Flask(__name__)
# CORS(app)

# # Initialize pipeline
# pipeline_data = run_pipeline("ml-latest-small/ml-latest-small/ratings.csv", "ml-latest-small/ml-latest-small/movies.csv")


# @app.route("/api/movies", methods=["GET"])
# def get_movies():
#     """Return all movie titles for autocomplete."""
#     return jsonify(pipeline_data["movie_titles"])


# @app.route("/api/content", methods=["GET"])
# def recommend_content():
#     """Content-based movie recommendations."""
#     movie_title = request.args.get("title")
#     if not movie_title:
#         return jsonify({"error": "Please provide a movie title"}), 400
#     recommendations = pipeline_data["content_model"].recommend(movie_title)
#     return jsonify({"recommendations": recommendations})


# @app.route("/api/collaborative", methods=["GET"])
# def recommend_collaborative():
#     """Collaborative-based movie recommendations."""
#     user_id = request.args.get("user_id")
#     if not user_id:
#         return jsonify({"error": "Please provide a user ID"}), 400
#     recommendations = pipeline_data["collaborative_model"].recommend(int(user_id))
#     return jsonify({"recommendations": recommendations})


# @app.route("/api/hybrid", methods=["GET"])
# def recommend_hybrid():
#     """
#     API endpoint for hybrid recommendations.
#     Requires both user_id and movie_title as input parameters.
#     """
#     user_id = request.args.get("user_id")
#     movie_title = request.args.get("title")

#     if not user_id or not movie_title:
#         return jsonify({"error": "Please provide both user ID and movie title"}), 400

#     try:
#         user_id = int(user_id)  # Ensure user_id is an integer
#         recommendations = pipeline_data["hybrid_model"].recommend(user_id, movie_title)
#         return jsonify({"recommendations": recommendations})
#     except Exception as e:
#         print(f"Error in hybrid recommendation: {e}")
#         return jsonify({"error": str(e)}), 500



# if __name__ == "__main__":
#     app.run(debug=True)
