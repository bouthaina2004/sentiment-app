# sentiment-app : dépôt du binôme

Application fil rouge du cours *Développement et déploiement d'applications intelligentes*.
Ce dépôt grandit chaque semaine ; la semaine 1 met en place le cadrage et l'environnement.

## Installer et utiliser le paquet de prédiction

L'installation client ne nécessite pas de cloner ce dépôt. Python 3.11 ou plus
récent est requis. Dans un environnement virtuel activé, installez la roue
publiée :

```powershell
python -m pip install "https://github.com/bouthaina2004/sentiment-app/releases/download/v1.0.1/sentiment_app-1.0.1-py3-none-any.whl"
```

Le paquet inclut son modèle. Utilisez la commande installée ou l'API Python :

```powershell
sentiment "Livraison rapide, très satisfait"
sentiment --json "Colis abîmé, service client injoignable"
sentiment --version
python -c "from sentiment_app import predict; print(predict('Produit conforme à la description'))"
python -m pip check
```

Les avis blancs sont refusés avec le code de sortie 2. Le classifieur peut
mal interpréter la négation, l'ironie ou les avis ambivalents ; son score n'est
pas une garantie de justesse. Consultez [README-PAQUET.md](README-PAQUET.md)
pour la documentation utilisateur complète.

## Installation (3 commandes)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell : .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Vérifier son installation

```bash
python scripts/check_setup.py    # diagnostic lisible : versions, dossiers, Git
pytest -q                        # mêmes vérifications sous forme de tests
```

La démarche complète de test, étape par étape, est dans `TESTS.md`.

## Structure

```text
sentiment-app/
├── README.md
├── TP1-ENONCE.md    # énoncé du TP de la semaine 1
├── TESTS.md         # démarche à suivre pour le test
├── requirements.txt
├── .gitignore
├── data/            # jeux de données (versionnés par DVC à partir de la semaine 7)
├── models/          # modèles entraînés (jamais dans Git)
├── app/             # API FastAPI (semaine 3)
├── ui/              # Streamlit (semaine 5)
├── tests/           # pytest (semaine 1 : tests d'environnement)
├── scripts/         # utilitaires (check_setup, nouveau cas de cadrage)
└── docs/cadrage/    # fiches de cadrage du TP1
```

## Membres du binôme

| Rôle | Nom | Identifiant GitHub | Travail de la semaine 1 |
| --- | --- | --- | --- |
| Membre A | Oumaima EL MANSOURI | https://github.com/oumaimaelmansouri01-svg/sentiment-app | Initialisation Git, installation des dépendances Python et rédaction des fiches de cadrage |
| Membre B | Bouthaina AZOUGAI| [@Boutaina2004] | Vérification des fiches, tests pytest et validation de l'environnement |
| Membre C | Meryem BAYARi| [@Kuromiav02] | Vérification des fiches, tests pytest et validation de l'environnement |