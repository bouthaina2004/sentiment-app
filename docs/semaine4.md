# Semaine 4 : tests approfondis et qualité, notes du binôme

> Une à deux pages. Chiffres relevés lors des exécutions locales du TP4.

## 1. Couverture

- Avant les nouveaux tests : 91 % de couverture de `api/`. Lignes manquantes de `api/main.py` : 49, 77–79 et 85–87.
- La ligne 49 correspondait au classifier non chargé (503), les lignes 77–79 à une panne de prédiction (500), et les lignes 85–87 au lanceur direct, non exécuté lorsque pytest importe l'application.
- Après les tests d'intégration : 98 %. Les deux lignes manquantes appartiennent au bloc lanceur direct `if __name__ == "__main__"` ; aucune ligne n'est exclue de la mesure.

## 2. Défauts trouvés

| Symptôme | Test qui l'a révélé | Correction |
| --- | --- | --- |
| Une chaîne d'espaces passait la contrainte de longueur du schéma et ne recevait pas la même forme de 422 qu'une chaîne vide. | `test_frontieres_du_contrat` et `test_tout_texte_de_blancs_est_refuse` (Hypothesis) | Validateur Pydantic appliquant `strip()` et produisant une erreur de validation standard. |
| Un `ValueError` interne du classifier était transformé en 422, comme s'il s'agissait d'une faute du client. | `test_panne_modele_repond_500_sans_detail_interne` | Toute exception de prédiction est journalisée côté serveur et renvoie un 500 générique. |
| Un avis sans mot connu du vocabulaire obtenait tout de même une étiquette binaire. | `test_texte_hors_vocabulaire_indetermine` | Seuil nommé à 0,60 : en dessous, l'API renvoie `INDETERMINE` en conservant le score. |
| Un modèle chargé avec des classes différentes du contrat pouvait produire une réponse invalide. | `test_demarrage_refuse_classes_inattendues` | Vérification des classes au démarrage et correspondance explicite entre étiquettes. |

## 3. Seuil d'abstention

- Seuil 0,50 : 58/58 réponses, exactitude 0,879, 7 erreurs, aucun avis envoyé à un humain.
- Seuil 0,60 : 42/58 réponses (72 %), exactitude 0,952, 2 erreurs parmi les réponses, 16 avis envoyés à un humain.
- Seuil 0,70 : 37/58 réponses (64 %), exactitude 1,000, aucune erreur parmi les réponses, 21 avis envoyés à un humain.
- Seuil retenu : 0,60. Il dirige 28 % des avis vers une vérification humaine et évite cinq des sept erreurs du modèle sans répondre à tout, avec moins d'abstentions qu'au seuil de 0,70.

## 4. Jeu d'or

- Jeu de contrôle proposé au binôme : 20 avis, dont 6 difficiles (négation, ironie, avis mitigés et domaine différent).
- Bilan : 13 avis justes, 6 abstentions et 1 erreur franche déclarée (`xfail` strict).
- L'erreur déclarée concerne une négation (« Je ne recommande pas… ») que le sac de mots ne rattache pas correctement à son contexte. Les abstentions portent notamment sur des formulations peu familières ou mitigées ; elles sont préférables à une réponse assurée mais fragile.

## 5. Outils statiques

- Avant correction : 20 remarques Ruff dans l'arbre de travail, dont 9 dans les copies de kits pédagogiques ; aucune remarque mypy. Les sources de kits non livrées ont été exclues, et les 11 remarques des fichiers du projet ont été corrigées.
- Après correction : `ruff check .` est propre ; `mypy api` répond « Success: no issues found in 4 source files ». Aucun des défauts de comportement (blancs seuls, erreur interne confondue avec une 422) n'avait été signalé par ces outils : les tests de propriétés et d'intégration sont donc nécessaires en complément.
