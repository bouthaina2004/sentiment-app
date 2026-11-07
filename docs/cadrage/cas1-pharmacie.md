# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)
Une pharmacie ou un groupement d'officines souhaite automatiser la détection des informations manquantes, illisibles ou ambiguës (posologie, durée, signature, identité) sur les ordonnances avant la délivrance des médicaments.

## Utilisateur final (obligatoire)
Le pharmacien titulaire ou le préparateur en pharmacie au comptoir lors de l'analyse de l'ordonnance.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [X] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)
L'approche par Machine Learning est privilégiée car (b) la présence des champs obligatoires est strictement vérifiable par rapport au cadre réglementaire de l'ordonnance, et (d) la conséquence d'une erreur (délivrance d'un traitement erroné ou incomplet) présente un risque critique pour la santé du patient.

## Données nécessaires et leur origine (obligatoire)
Un corpus historique d'ordonnances numérisées et anonymisées, étiquetées par des professionnels de santé pour identifier la présence ou l'absence des mentions légales obligatoires.

## Métrique de succès et seuil d'acceptation (obligatoire)
Un taux de rappel (recall) supérieur à 98 % sur la détection des champs obligatoires manquants, afin de réduire au maximum le nombre de faux négatifs (ordonnances incomplètes non signalées).

## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Un faux négatif peut conduire à une erreur de dispensation médicamenteuse avec un impact sanitaire grave. Par conséquent, le système agit uniquement en tant qu'assistant d'alerte et la validation finale de l'ordonnance demeure sous la responsabilité exclusive du pharmacien.

## Risques éthiques ou de confidentialité (obligatoire)
Traitement massif de données de santé à caractère personnel soumis à des exigences strictes de conformité (RGPD, hébergement agréé HDS et anonymisation des documents manipulés).

## Approche écartée et pourquoi (facultatif)
L'utilisation d'un modèle génératif seul a été écartée en raison des risques d'hallucination et d'imprécision inacceptables lorsqu'il s'agit d'interpréter des données de santé critiques.
