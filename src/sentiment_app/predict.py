"""Interface publique de prédiction du paquet sentiment-app."""

from functools import lru_cache
from importlib.resources import files
from typing import TypedDict

import joblib


class Resultat(TypedDict):
    label: str
    score: float


@lru_cache(maxsize=1)
def charger_modele():
    """Charge le modèle embarqué dans la distribution installée."""
    modele = files("sentiment_app").joinpath("modele/sentiment.joblib")
    with modele.open("rb") as fichier:
        return joblib.load(fichier)


def predict(texte: str) -> Resultat:
    """Renvoie le label du modèle et son score de confiance."""
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    modele = charger_modele()
    return {
        "label": str(modele.predict([texte])[0]),
        "score": round(float(modele.predict_proba([texte]).max()), 4),
    }
