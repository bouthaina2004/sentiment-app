# Journal des modifications

## [1.0.1] - 2026-11-13

- Ajout du mode de construction depuis un tag Git sans commiter le modèle.
- Vérification de l'installation de la roue et de la distribution source.
- Documentation client complétée dans `README.md`.

## [1.0.0] - 2026-11-13

- Ajout du paquet installable `sentiment-app` et de la fonction publique `predict`.
- Inclusion du modèle entraîné dans la distribution wheel.
- Ajout de la commande `sentiment` avec sorties texte et JSON.
- Limites connues : le classifieur TF-IDF peut mal interpréter la négation,
  l'ironie et les avis ambivalents ; le score n'est pas une garantie de justesse.
