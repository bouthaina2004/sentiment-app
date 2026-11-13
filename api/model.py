"""Raccord entre l'API et le modèle entraîné au TP2.

L'API n'entraîne rien et ne connaît pas scikit-learn : elle appelle la fonction
predict() de src/predict.py, qui charge models/sentiment.joblib une seule fois.
"""
from typing import Literal, TypedDict

from src.predict import charger_modele
from src.predict import predict as _predict

SentimentLabel = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]
ETIQUETTES: dict[str, SentimentLabel] = {"positive": "POSITIVE", "negative": "NEGATIVE"}
SEUIL_ABSTENTION = 0.60


class Classification(TypedDict):
    label: SentimentLabel
    score: float
    text: str


class SentimentClassifier:
    """Enveloppe du modèle TP2 avec l'interface attendue par l'API."""

    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        pipeline = charger_modele()  # échoue immédiatement si le joblib manque
        classes = set(pipeline.classes_)
        if classes != set(ETIQUETTES):
            raise ValueError(f"classes du modèle inattendues : {sorted(classes)}")

    def predict(self, text: str) -> Classification:
        """Renvoie le verdict du contrat, la confiance et un aperçu du texte."""
        resultat = _predict(text)
        label: SentimentLabel = ETIQUETTES[resultat["label"]]
        if resultat["score"] < SEUIL_ABSTENTION:
            label = "INDETERMINE"
        return {"label": label, "score": resultat["score"], "text": text[:100]}


def load_model() -> SentimentClassifier:
    """Construit le classifier (le cache de chargement est dans src/predict.py)."""
    return SentimentClassifier()
