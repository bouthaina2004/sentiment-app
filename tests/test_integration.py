"""Tests d'intégration : l'API telle qu'elle tourne vraiment (TP4, étape D).

Les tests du TP3 vérifient des réponses ; ceux-ci vérifient le démarrage de l'API
et son comportement quand le modèle manque ou tombe en panne.
"""
from pathlib import Path

import pytest

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


def test_demarrage_reel_charge_le_modele():
    """D.1 (donné en exemple) : un client ouvert par « with » exécute le lifespan."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        reponse = client.get("/health")
    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_demarrage_refuse_si_modele_absent(monkeypatch, tmp_path):
    from fastapi.testclient import TestClient

    from api.main import app
    from src import predict

    monkeypatch.setattr(predict, "MODELE", tmp_path / "absent.joblib")
    predict.charger_modele.cache_clear()
    try:
        with pytest.raises(FileNotFoundError, match="sentiment.joblib absent"):
            with TestClient(app):
                pass
    finally:
        predict.charger_modele.cache_clear()


def test_modele_non_charge_repond_503(monkeypatch):
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        monkeypatch.setattr(app.state, "classifier", None)
        assert client.get("/health").status_code == 503
        assert client.post("/predict", json={"text": "avis"}).status_code == 503


@pytest.mark.parametrize("erreur", [RuntimeError("secret"), ValueError("bug interne")])
def test_panne_modele_repond_500_sans_detail_interne(monkeypatch, erreur):
    from types import SimpleNamespace
    from unittest.mock import Mock

    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        monkeypatch.setattr(
            app.state,
            "classifier",
            SimpleNamespace(model_name="modèle simulé", predict=Mock(side_effect=erreur)),
        )
        reponse = client.post("/predict", json={"text": "avis valide"})
    assert reponse.status_code == 500
    assert reponse.json()["detail"] == "Erreur interne du serveur"
    assert str(erreur) not in reponse.text


def test_demarrage_refuse_classes_inattendues(monkeypatch):
    from types import SimpleNamespace

    from api import model

    monkeypatch.setattr(
        model,
        "charger_modele",
        lambda: SimpleNamespace(classes_=["negative", "neutral", "positive"]),
    )
    with pytest.raises(ValueError, match="classes du modèle inattendues"):
        model.SentimentClassifier()
