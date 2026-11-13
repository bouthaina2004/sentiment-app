# Fiche de cadrage : Questions sur le règlement intérieur

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)
Une organisation souhaite mettre en place un assistant textuel capable de répondre de manière précise et automatisée aux questions des collaborateurs concernant les règles, procédures et consignes inscrites dans le règlement intérieur.

## Utilisateur final (obligatoire)
Le collaborateur ou le département des ressources humaines (RH) recherchant une information rapide et fiable sur une disposition spécifique du règlement.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [ ] Machine learning
- [x] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)
L'approche par RAG (Retrieval-Augmented Generation) est retenue car (b) chaque réponse générée est directement vérifiable et traçable par rapport aux extraits officiels du règlement sourcés, et (c) le coût par requête reste faible tout en garantissant l'accès à une documentation textuelle évolutive sans réentraînement complet du modèle.

## Données nécessaires et leur origine (obligatoire)
Le document officiel du règlement intérieur de l'entreprise au format texte ou PDF, ainsi que les éventuelles notes de service et annexes réglementaires en vigueur.

## Métrique de succès et seuil d'acceptation (obligatoire)
Un taux de pertinence des documents récupérés (Precision) supérieur à 90 % et une absence totale d'hallucination sur les articles cités lors des tests d'évaluation par questions-réponses de référence.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Une erreur d'interprétation ou une réponse erronée peut induire le salarié en erreur sur ses droits ou ses obligations disciplinaires. C'est pourquoi le système fournit systématiquement le lien vers l'article source et l'outil est positionné comme une aide à l'information, avec un renvoi explicite vers le service RH pour les cas complexes.

## Risques éthiques ou de confidentialité (obligatoire)
Risque d'accès non autorisé à des notes de service internes ou de mauvaise interprétation de clauses disciplinaires, nécessitant de restreindre la base documentaire aux documents officiels et validés par la direction.

## Approche écartée et pourquoi (facultatif)
L'approche par modèle génératif seul a été écartée en raison du risque élevé d'hallucination, qui pourrait amener le modèle à inventer des règles ou des sanctions non prévues par le cadre légal de l'entreprise.
