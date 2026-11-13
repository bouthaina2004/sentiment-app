# Semaine 5 : l'interface, notes du binôme

> Trois questions, quelques phrases chacune. Répondez avec ce que vous avez observé.

## 1. Pourquoi l'interface n'importe-t-elle jamais `predict()` ni le fichier `.joblib` ?

L'interface est un client HTTP indépendant : elle parle uniquement à l'API via `ui.client`. Ainsi, le modèle et son fichier `.joblib` restent côté serveur ; réentraîner ou remplacer le modèle ne demande pas de changer la page.

## 2. Que montre l'interface quand le modèle hésite, et pourquoi est-ce mieux qu'un verdict forcé ?

Pour un score sous le seuil, l'interface affiche « Je ne sais pas : à faire vérifier par un humain » et rappelle que la confiance est sous le seuil d'abstention. Cela évite de présenter une prédiction incertaine comme une certitude et permet une décision humaine.

## 3. Que voit l'utilisateur quand l'API tombe ? Et le fichier `data/avis_exemple.csv` : combien d'avis partent vers un humain ?

Si l'API est arrêtée, la page affiche « API injoignable : lancez d'abord uvicorn api.main:app ». Sur `data/avis_exemple.csv`, le résumé observé est `{'INDETERMINE': 1, 'NEGATIVE': 2, 'POSITIVE': 3}` : un avis sur six est donc envoyé à un humain.
