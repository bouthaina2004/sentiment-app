# Semaine 3 : l'API, notes du binôme

> Deux questions, quelques phrases chacune. Répondez avec ce que vous avez observé, pas avec le cours.

## 1. Pourquoi l'API refuse-t-elle de démarrer sans `models/sentiment.joblib`, plutôt que de démarrer et de répondre 503 ?

Le `lifespan` charge le modèle avant d'accepter des requêtes. En retirant temporairement `models/sentiment.joblib`, j'ai observé un `FileNotFoundError` au démarrage : cela évite de signaler un service prêt alors que toutes les prédictions échoueraient. Un code 503 serait plus adapté si l'API pouvait rester utile sans modèle ou si celui-ci pouvait être rechargé à chaud.

## 2. Un texte vide est refusé deux fois : par Pydantic, puis par `predict()`. Est-ce redondant ?

Ce n'est pas une redondance inutile : Pydantic vérifie le contrat HTTP et renvoie 422 avant d'appeler le modèle, tandis que `predict()` protège aussi les appels directs hors de l'API. J'ai également testé une chaîne composée d'espaces : elle passe la longueur minimale de Pydantic, puis `predict()` la refuse. Les deux validations empêchent donc des entrées invalides à des niveaux différents.
