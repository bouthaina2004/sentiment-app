"""Vérifie qu'une release du paquet fonctionne depuis une installation neuve."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import venv
import zipfile
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
DIST = RACINE / "dist"
VERSION = "1.0.1"
ROUE = f"sentiment_app-{VERSION}-py3-none-any.whl"
SOURCE = f"sentiment_app-{VERSION}.tar.gz"
RAPPORT = RACINE / "docs" / "livrable-tp4.txt"


def lancer(commande: list[str], cwd: Path = RACINE) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        commande,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def verifier(
    condition: bool,
    message: str,
    erreurs: list[str],
    controles: list[str],
) -> None:
    statut = "OK" if condition else "ÉCHEC"
    print(f"[{statut}] {message}")
    controles.append(f"{statut} — {message}")
    if not condition:
        erreurs.append(message)


def python_venv(env_dir: Path) -> Path:
    return env_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def main() -> int:
    erreurs: list[str] = []
    controles: list[str] = []
    roue_path = DIST / ROUE
    source_path = DIST / SOURCE
    verifier(roue_path.is_file(), f"roue présente : {ROUE}", erreurs, controles)
    verifier(source_path.is_file(), f"distribution source présente : {SOURCE}", erreurs, controles)
    verifier(
        DIST.is_dir() and sorted(p.name for p in DIST.iterdir()) == sorted([ROUE, SOURCE]),
        "aucun autre fichier dans dist/",
        erreurs,
        controles,
    )
    verifier(
        (RACINE / "CHANGELOG.md").is_file()
        and f"[{VERSION}]" in (RACINE / "CHANGELOG.md").read_text(encoding="utf-8"),
        f"CHANGELOG.md décrit cette version : [{VERSION}]",
        erreurs,
        controles,
    )

    commande_tag = lancer(["git", "describe", "--exact-match", "--tags", "HEAD"])
    verifier(
        commande_tag.returncode == 0 and commande_tag.stdout.strip() == f"v{VERSION}",
        f"étiquette Git sur le dernier commit : v{VERSION}",
        erreurs,
        controles,
    )

    if roue_path.is_file():
        try:
            with zipfile.ZipFile(roue_path) as archive:
                contenu = archive.namelist()
            verifier(
                any(n.endswith("/modele/sentiment.joblib") for n in contenu),
                "modèle embarqué dans la roue",
                erreurs,
                controles,
            )
            verifier(
                any(n.endswith(".dist-info/entry_points.txt") for n in contenu),
                "commande « sentiment » déclarée",
                erreurs,
                controles,
            )
            verifier(
                not any("/tests/" in n or n.startswith("tests/") for n in contenu),
                "pas de tests dans la roue",
                erreurs,
                controles,
            )
        except zipfile.BadZipFile:
            verifier(False, "la roue est une archive ZIP valide", erreurs, controles)
    if source_path.is_file():
        try:
            import tarfile

            with tarfile.open(source_path, "r:gz") as archive:
                contenu_source = archive.getnames()
            verifier(
                any(n.endswith("/src/sentiment_app/modele/sentiment.joblib") for n in contenu_source),
                "modèle embarqué dans la distribution source",
                erreurs,
                controles,
            )
        except tarfile.TarError:
            verifier(False, "la distribution source est une archive tar.gz valide", erreurs, controles)

    if not erreurs:
        with tempfile.TemporaryDirectory(prefix="sentiment-app-verification-") as temp:
            for label, distribution in (("roue", roue_path), ("source", source_path)):
                env_dir = Path(temp) / f"venv-{label}"
                venv.EnvBuilder(with_pip=True).create(env_dir)
                python = python_venv(env_dir)
                installation = lancer(
                    [str(python), "-m", "pip", "install", f"{distribution}[test]"]
                )
                if installation.returncode != 0:
                    print(installation.stdout, end="")
                    print(installation.stderr, file=sys.stderr, end="")
                verifier(
                    installation.returncode == 0,
                    f"installation depuis la distribution {label} dans un environnement neuf",
                    erreurs,
                    controles,
                )
                if installation.returncode == 0:
                    env = {**os.environ, "VERIFICATION_LIVRABLE": "1"}
                    tests = subprocess.run(
                        [str(python), "-m", "pytest", "-q", "tests/test_paquet.py"],
                        cwd=RACINE,
                        env=env,
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    print(tests.stdout, end="")
                    if tests.stderr:
                        print(tests.stderr, file=sys.stderr, end="")
                    verifier(
                        tests.returncode == 0,
                        f"tests lancés sur le paquet installé depuis la distribution {label}",
                        erreurs,
                        controles,
                    )
                    verifier(
                        lancer([str(python), "-m", "pip", "check"]).returncode == 0,
                        f"dépendances cohérentes après installation depuis {label}",
                        erreurs,
                        controles,
                    )
                    if tests.returncode == 0 and label == "roue":
                        commande = env_dir / (
                            "Scripts/sentiment.exe" if os.name == "nt" else "bin/sentiment"
                        )
                        resultat = lancer(
                            [str(commande), "--json", "Produit cassé et très décevant"]
                        )
                        verifier(
                            resultat.returncode == 0
                            and '"label": "negative"' in resultat.stdout,
                            f"commande installée : {resultat.stdout.strip()}",
                            erreurs,
                            controles,
                        )

    rapport = "\n".join(
        [
            f"Vérification du livrable sentiment-app {VERSION}",
            *controles,
            f"Bilan : {'NON CONFORME' if erreurs else 'CONFORME'}",
            "",
        ]
    )
    RAPPORT.parent.mkdir(parents=True, exist_ok=True)
    RAPPORT.write_text(rapport, encoding="utf-8")
    print(f"Bilan : {'NON CONFORME' if erreurs else 'CONFORME'}")
    print(f"Rapport : {RAPPORT.relative_to(RACINE)}")
    return 1 if erreurs else 0


if __name__ == "__main__":
    raise SystemExit(main())
