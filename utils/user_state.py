# utils/user_state.py

# Dictionnaire temporaire pour stocker les scores utilisateurs
user_scores = {}  # clé = user_id (int), valeur = score (int)

# Score maximum avant de débloquer les vocaux
SCORE_MAX = 5

def get_score(user_id):
    """Retourne le score actuel de l'utilisateur."""
    return user_scores.get(user_id, 0)

def increment_score(user_id):
    """Ajoute 1 point au score utilisateur (jusqu'à SCORE_MAX)."""
    score = user_scores.get(user_id, 0)
    if score < SCORE_MAX:
        user_scores[user_id] = score + 1
    return user_scores[user_id]

def reset_score(user_id):
    """Réinitialise le score utilisateur (ex : en début de phase 2)."""
    user_scores[user_id] = 0
