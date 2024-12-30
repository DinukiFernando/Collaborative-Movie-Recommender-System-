# import pandas as pd


# def load_data(ratings_path, movies_path):
#     ratings = pd.read_csv(ratings_path)
#     movies = pd.read_csv(movies_path)
#     movies["genres"] = movies["genres"].str.replace("|", " ", regex=False)
#     return ratings, movies


import pandas as pd


def load_data(ratings_path, movies_path):
    ratings = pd.read_csv(ratings_path)
    movies = pd.read_csv(movies_path)
    movies["genres"] = movies["genres"].str.replace("|", " ", regex=False)
    return ratings, movies


