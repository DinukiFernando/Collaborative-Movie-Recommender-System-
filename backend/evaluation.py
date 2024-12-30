# from sklearn.metrics import precision_score, recall_score
# from surprise import accuracy


# def evaluate_content_model(recommendations, ground_truth):
#     """
#     Evaluate the content-based model using precision and recall.
#     :param recommendations: List of recommended movie titles.
#     :param ground_truth: List of ground truth movie titles.
#     :return: Precision and Recall scores.
#     """
#     recommended_set = set([rec["title"].strip().lower() for rec in recommendations])
#     ground_truth_set = set([title.strip().lower() for title in ground_truth])

#     if not recommended_set or not ground_truth_set:
#         return 0.0, 0.0

#     true_positives = recommended_set & ground_truth_set
#     precision = len(true_positives) / len(recommended_set) if recommended_set else 0.0
#     recall = len(true_positives) / len(ground_truth_set) if ground_truth_set else 0.0

#     return precision, recall


# def evaluate_collaborative_model(model, testset):
#     """
#     Evaluate the collaborative model using RMSE and MAE.
#     :param model: Collaborative model to evaluate.
#     :param testset: Test set to evaluate the model on.
#     :return: Dictionary containing RMSE and MAE.
#     """
#     predictions = model.model.test(testset)
#     rmse = accuracy.rmse(predictions, verbose=False)
#     mae = accuracy.mae(predictions, verbose=False)
#     return {"RMSE": rmse, "MAE": mae}


from sklearn.metrics import precision_score, recall_score
from surprise import accuracy


def evaluate_collaborative_model(model, testset):
    predictions = model.test(testset)
    rmse = accuracy.rmse(predictions)
    mae = accuracy.mae(predictions)
    return {"RMSE": rmse, "MAE": mae}


def evaluate_content_model(recommendations, ground_truth):
    recommended_set = set(recommendations)
    ground_truth_set = set(ground_truth)

    true_positives = len(recommended_set & ground_truth_set)
    precision = true_positives / len(recommended_set) if recommended_set else 0
    recall = true_positives / len(ground_truth_set) if ground_truth_set else 0
    return precision, recall
