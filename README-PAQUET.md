# sentiment-app

Paquet Python autonome pour classer en français un avis client comme `positive`
ou `negative`, avec un score de confiance. Le modèle est inclus dans la roue :
il n'est pas nécessaire de cloner le dépôt ni de télécharger un fichier modèle à
part.

## Installation

Installez la roue `sentiment_app-1.0.0-py3-none-any.whl` publiée dans la release
GitHub du projet :

```powershell
python -m pip install .\sentiment_app-1.0.0-py3-none-any.whl
```

Le paquet nécessite Python 3.11 ou plus récent. Scikit-learn est fixé à la
série 1.5, compatible avec le modèle sérialisé.

## Utilisation Python

```python
from sentiment_app import predict

print(predict("Livraison rapide, produit conforme et très satisfaisant"))
# {'label': 'positive', 'score': 0.78}
```

Les chaînes vides ou ne contenant que des espaces déclenchent `ValueError`.

## Utilisation en ligne de commande

```powershell
sentiment "Produit cassé et service injoignable"
sentiment --json "Livraison rapide et excellente"
```

La commande affiche le label et le score (ou du JSON avec `--json`). Le score
est la confiance du classifieur, pas une garantie de justesse. Le modèle TF-IDF
et régression logistique ne comprend pas toujours les négations, l'ironie ou les
avis ambivalents ; les résultats incertains doivent être vérifiés par un humain.
