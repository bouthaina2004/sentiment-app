"""Pose les étapes ajoutées aux TP2, TP4, TP5 et TP6 sur votre dépôt, sans rien écraser.

    python appliquer_complements.py CHEMIN_DU_DEPOT --etape tp2 --simulation
    python appliquer_complements.py CHEMIN_DU_DEPOT --etape tp2
    python appliquer_complements.py CHEMIN_DU_DEPOT --etape toutes      # dépôt déjà en fin de TP6

Étapes : tp2 (explicabilité), tp4 (biais), tp5 (graphiques), tp6 (fiche modèle). Chaque étape vérifie
que le TP correspondant est installé. Un fichier déjà présent n'est jamais remplacé : il est signalé.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent

ETAPES = {
    "tp2": {
        "dossier": "tp2-explicabilite",
        "titre": "TP2, étape F : ce que regarde le modèle",
        "prerequis": ["src/train.py"],
        "fichiers": ["src/expliquer.py", "tests/test_explicabilite.py"],
    },
    "tp4": {
        "dossier": "tp4-biais",
        "titre": "TP4, étape F : le modèle sert-il tous les avis de la même façon ?",
        "prerequis": ["src/train.py", "api/model.py"],
        "fichiers": ["src/biais.py", "tests/test_biais.py"],
    },
    "tp5": {
        "dossier": "tp5-graphiques",
        "titre": "TP5, étape G : deux graphiques dans l'onglet fichier",
        "prerequis": ["ui/app.py", "ui/client.py"],
        "fichiers": ["ui/graphiques.py", "tests/test_graphiques.py"],
    },
    "tp6": {
        "dossier": "tp6-fiche-modele",
        "titre": "TP6, étape G : la fiche modèle",
        "prerequis": ["sentiment_app/__init__.py", "models/metrics.json"],
        "fichiers": ["docs/fiche-modele.md", "tests/test_fiche_modele.py"],
    },
}

IMPORT_AVANT = "from ui import client\n"
IMPORT_APRES = "from ui import client, graphiques\n"
ANCRE_PAGE = "            st.write(client.resumer(reponses))\n"
BLOC_PAGE = (
    "            colonne_verdicts, colonne_confiances = st.columns(2)\n"
    "            colonne_verdicts.caption(\"Répartition des verdicts\")\n"
    "            colonne_verdicts.bar_chart(graphiques.repartition(reponses))\n"
    "            colonne_confiances.caption(\"Confiance du modèle, par tranche\")\n"
    "            colonne_confiances.bar_chart(graphiques.histogramme_confiances(reponses))\n"
)
SHAP = '"shap==0.46.*"'
PYTEST = '"pytest==8.3.*"'


def copier(depot: Path, dossier: str, relatif: str, simulation: bool) -> str:
    source, cible = KIT / dossier / relatif, depot / relatif
    if cible.exists():
        if cible.read_bytes() == source.read_bytes():
            return f"  = {relatif} : déjà en place"
        return f"  ! {relatif} : déjà présent et différent, laissé tel quel"
    if not simulation:
        cible.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, cible)
    return f"  + {relatif}"


def brancher_graphiques(depot: Path, simulation: bool) -> str:
    page = depot / "ui" / "app.py"
    texte = page.read_text(encoding="utf-8")
    if "graphiques.repartition" in texte:
        return "  = ui/app.py : graphiques déjà branchés"
    if texte.count(IMPORT_AVANT) != 1 or texte.count(ANCRE_PAGE) != 1:
        return ("  ! ui/app.py : page modifiée, branchement à faire à la main (voir la marche à suivre) :\n"
                "    importer graphiques à côté de client, puis, sous st.write(client.resumer(reponses)) :\n"
                + "".join("    " + ligne for ligne in BLOC_PAGE.splitlines(keepends=True)))
    if not simulation:
        texte = texte.replace(IMPORT_AVANT, IMPORT_APRES, 1).replace(ANCRE_PAGE, ANCRE_PAGE + BLOC_PAGE, 1)
        page.write_text(texte, encoding="utf-8")
    return "  ~ ui/app.py : import de graphiques, cinq lignes sous le résumé"


def adapter_la_ci(depot: Path, simulation: bool) -> list[str]:
    """Épingle pytest comme dans requirements.txt, et ajoute SHAP, sur la ligne d'installation de la CI.

    Sans épinglage, la CI installe pytest 9, dont monkeypatch ne restaure plus un attribut de
    app.state : un test du TP5 laisse alors l'API sans modèle, et les suivants échouent.
    """
    ci = depot / ".github" / "workflows" / "ci.yml"
    if not ci.exists():
        return ["  ! .github/workflows/ci.yml absent : rien à adapter"]
    lignes = ci.read_text(encoding="utf-8").splitlines(keepends=True)
    for i, ligne in enumerate(lignes):
        if "pip install pandas" not in ligne:
            continue
        messages, nouvelle = [], ligne.rstrip("\n")
        if PYTEST not in nouvelle and " pytest " in nouvelle + " ":
            nouvelle = (nouvelle + " ").replace(" pytest ", f" {PYTEST} ", 1).rstrip()
            messages.append(f"  ~ CI : pytest épinglé, {PYTEST}")
        if SHAP not in nouvelle:
            nouvelle += f" {SHAP}"
            messages.append(f"  ~ CI : {SHAP} ajouté à l'installation des dépendances")
        if not messages:
            return ["  = CI : déjà adaptée"]
        if not simulation:
            lignes[i] = nouvelle + "\n"
            ci.write_text("".join(lignes), encoding="utf-8")
        return messages
    return ["  ! CI : ligne « pip install pandas ... » introuvable : épinglez pytest et ajoutez SHAP à la main"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("depot", type=Path)
    parser.add_argument("--etape", choices=[*ETAPES, "toutes"], required=True)
    parser.add_argument("--simulation", action="store_true", help="afficher sans rien modifier")
    args = parser.parse_args()
    depot = args.depot.resolve()
    if not (depot / ".git").exists():
        print(f"{depot} n'est pas un dépôt Git : indiquez la racine de sentiment-app.", file=sys.stderr)
        return 1
    choisies = list(ETAPES) if args.etape == "toutes" else [args.etape]
    print(("Simulation : rien ne sera modifié.\n" if args.simulation else "") + f"Dépôt : {depot}")
    erreurs = 0
    for nom in choisies:
        etape = ETAPES[nom]
        print(f"\n{etape['titre']}")
        manquants = [p for p in etape["prerequis"] if not (depot / p).exists()]
        if manquants:
            print(f"  ! étape ignorée : {', '.join(manquants)} absent ; installez d'abord le TP concerné")
            erreurs += 1
            continue
        for relatif in etape["fichiers"]:
            print(copier(depot, etape["dossier"], relatif, args.simulation))
        if nom == "tp5":
            print(brancher_graphiques(depot, args.simulation))
    print("\nIntégration continue")
    print("\n".join(adapter_la_ci(depot, args.simulation)))
    print("\nEnsuite : python -m pytest -q, puis la marche à suivre de chaque étape.")
    return 1 if erreurs else 0


if __name__ == "__main__":
    raise SystemExit(main())
