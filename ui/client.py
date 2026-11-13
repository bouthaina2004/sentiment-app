"""Client HTTP de l'API (TP5) : tout ce que l'interface sait de l'API passe par ce module.

L'interface n'importe jamais predict() ni le fichier .joblib : elle envoie des requêtes à
l'API du TP3, corrigée au TP4, et traduit chaque réponse en message pour l'utilisateur.
"""
import os
from collections import Counter
from dataclasses import dataclass

import httpx

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")
BACKEND = os.environ.get("SENTIMENT_BACKEND", "api")
VERDICTS = {
    "POSITIVE": "Avis positif",
    "NEGATIVE": "Avis négatif",
    "INDETERMINE": "Je ne sais pas : à faire vérifier par un humain",
}
SEUIL_ABSTENTION = 0.60
INJOIGNABLE = "API injoignable : lancez d'abord uvicorn api.main:app"
REFUS = "Texte refusé : vide, fait d'espaces, ou de plus de 2000 caractères."
SANS_MODELE = "Modèle non chargé : python src/train.py, puis relancer l'API."


@dataclass
class Reponse:
    """Ce que l'interface affiche : un verdict, ou un message d'erreur lisible."""

    ok: bool
    label: str | None = None
    score: float | None = None
    message: str = ""


def configurer(backend: str, api_url: str | None = None) -> None:
    """Configure l'API locale ou le modèle livré avec le paquet."""
    if backend not in {"api", "package"}:
        raise ValueError("SENTIMENT_BACKEND doit valoir 'api' ou 'package'")
    global BACKEND, API_URL
    BACKEND = backend
    if api_url:
        API_URL = api_url


def creer_session() -> httpx.Client | None:
    """La connexion HTTP est absente quand le modèle embarqué est utilisé."""
    if BACKEND == "package":
        return None
    return httpx.Client(base_url=API_URL, timeout=10)


def _predire_paquet(texte: str) -> Reponse:
    from sentiment_app import predict

    resultat = predict(texte)
    label = resultat["label"].upper()
    if resultat["score"] < SEUIL_ABSTENTION:
        label = "INDETERMINE"
    return Reponse(True, label=label, score=resultat["score"])


def sante(session: httpx.Client | None) -> Reponse:
    if BACKEND == "package":
        from sentiment_app import __version__, predict

        predict("Avis de vérification du chargement du modèle")
        return Reponse(True, message=f"modèle du paquet sentiment-app {__version__}")
    if session is None:
        raise ValueError("une session HTTP est nécessaire pour le backend API")
    try:
        r = session.get("/health")
    except httpx.TransportError:
        return Reponse(False, message=INJOIGNABLE)
    if r.status_code == 200:
        return Reponse(True, message=r.json()["model"])
    return Reponse(False, message=SANS_MODELE if r.status_code == 503 else f"Erreur de l'API ({r.status_code}).")


def predire(session: httpx.Client | None, texte: str) -> Reponse:
    if not texte.strip() or len(texte) > 2000:
        return Reponse(False, message=REFUS)
    if BACKEND == "package":
        return _predire_paquet(texte)
    if session is None:
        raise ValueError("une session HTTP est nécessaire pour le backend API")
    try:
        r = session.post("/predict", json={"text": texte})
    except httpx.TransportError:
        return Reponse(False, message=INJOIGNABLE)
    if r.status_code == 200:
        corps = r.json()
        return Reponse(True, label=corps["label"], score=corps["score"])
    if r.status_code == 422:
        return Reponse(False, message=REFUS)
    if r.status_code == 503:
        return Reponse(False, message=SANS_MODELE)
    return Reponse(False, message=f"Erreur interne de l'API ({r.status_code}).")


def predire_lot(session: httpx.Client | None, textes: list[str]) -> list[Reponse]:
    return [predire(session, texte) for texte in textes]


def resumer(reponses: list[Reponse]) -> dict[str, int]:
    """Nombre d'avis par verdict ; les refus et les erreurs sont comptés à part."""
    compte = Counter(r.label if r.ok else "REFUS OU ERREUR" for r in reponses)
    return dict(sorted(compte.items()))
