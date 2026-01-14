import math
from collections import defaultdict


def build_matrices(interactions):
    users = sorted({row["user"] for row in interactions})
    items = sorted({row["item"] for row in interactions})
    user_index = {user: idx for idx, user in enumerate(users)}
    item_index = {item: idx for idx, item in enumerate(items)}

    matrix = [[0.0 for _ in items] for _ in users]
    for row in interactions:
        u = user_index[row["user"]]
        i = item_index[row["item"]]
        matrix[u][i] = row.get("rating", 1.0)

    return users, items, matrix


def cosine(vec_a, vec_b):
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def build_item_similarity(matrix):
    if not matrix:
        return []
    num_users = len(matrix)
    num_items = len(matrix[0])
    item_vectors = [[matrix[u][i] for u in range(num_users)] for i in range(num_items)]
    similarity = [[0.0 for _ in range(num_items)] for _ in range(num_items)]
    for i in range(num_items):
        for j in range(num_items):
            if i == j:
                continue
            similarity[i][j] = cosine(item_vectors[i], item_vectors[j])
    return similarity


def recommend(user_idx, matrix, similarity, top_k=3):
    user_vector = matrix[user_idx]
    scores = defaultdict(float)
    for item_idx, rating in enumerate(user_vector):
        if rating == 0:
            continue
        for other_idx, sim in enumerate(similarity[item_idx]):
            if user_vector[other_idx] > 0:
                continue
            scores[other_idx] += sim * rating
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return ranked[:top_k]
