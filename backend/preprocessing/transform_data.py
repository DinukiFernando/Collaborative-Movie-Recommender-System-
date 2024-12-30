from sklearn.metrics.pairwise import cosine_similarity

def compute_item_similarity(ratings):
    """Compute item-item similarity matrix."""
    pivot_table = ratings.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)
    return cosine_similarity(pivot_table.T)
