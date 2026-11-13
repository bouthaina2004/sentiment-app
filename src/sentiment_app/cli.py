"""Commande en ligne sentiment."""

import argparse
import json
import sys

from sentiment_app import __version__, predict


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sentiment",
        description="Classe le sentiment d'un avis en français.",
    )
    parser.add_argument("texte", nargs="+", help="l'avis à classer")
    parser.add_argument("--json", action="store_true", help="sortie JSON")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    args = parser.parse_args(argv)
    try:
        resultat = predict(" ".join(args.texte))
    except ValueError as erreur:
        print(f"erreur : {erreur}", file=sys.stderr)
        return 2
    sortie = (
        json.dumps(resultat, ensure_ascii=False)
        if args.json
        else f"{resultat['label']} (confiance {resultat['score']:.0%})"
    )
    print(sortie)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
