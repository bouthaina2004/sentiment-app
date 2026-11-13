"""Tests de la distribution installée, exécutés par scripts/verifier_livrable.py."""

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_spec = importlib.util.find_spec("sentiment_app")
if not (_spec and "site-packages" in (_spec.origin or "")) and not os.environ.get(
    "VERIFICATION_LIVRABLE"
):
    pytest.skip(
        "paquet installé requis : python scripts/verifier_livrable.py",
        allow_module_level=True,
    )

import sentiment_app  # noqa: E402

COMMANDE = shutil.which("sentiment", path=str(Path(sys.executable).parent))


def test_importe_depuis_le_paquet_installe() -> None:
    assert "site-packages" in (sentiment_app.__file__ or "")
    assert sentiment_app.__version__ == "1.0.0"


def test_prediction_positive_et_score_valide() -> None:
    resultat = sentiment_app.predict("Très bon produit, livraison rapide et excellent service")
    assert resultat["label"] == "positive"
    assert 0.0 <= resultat["score"] <= 1.0


def test_prediction_negative_et_score_valide() -> None:
    resultat = sentiment_app.predict("Produit cassé, très mauvais et décevant")
    assert resultat["label"] == "negative"
    assert 0.0 <= resultat["score"] <= 1.0


@pytest.mark.parametrize("texte", ["", "   ", "\n\t"])
def test_refuse_les_textes_vides(texte: str) -> None:
    with pytest.raises(ValueError, match="texte vide"):
        sentiment_app.predict(texte)


def test_commande_installee_fonctionne_en_json() -> None:
    assert COMMANDE is not None, "la commande sentiment doit être installée"
    resultat = subprocess.run(
        [COMMANDE, "--json", "Très bon produit"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert '"label": "positive"' in resultat.stdout
