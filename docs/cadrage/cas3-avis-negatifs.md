# Fiche de cadrage : Priorisation des avis négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)
Une entreprise souhaite automatiser l'analyse, la classification et la priorisation des avis clients négatifs afin d'identifier rapidement les réclamations critiques et d'accélérer leur traitement par le service support.

## Utilisateur final (obligatoire)
Le responsable du service client ou les agents de support qualité chargés du traitement des litiges et des réclamations.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)
L'approche par Machine Learning (classification supervisée de textes) est retenue car (a) l'entreprise dispose d'un historique important d'avis étiquetés par niveau de criticité, et (d) la conséquence d'une erreur (classer par erreur un avis critique en mineur) entraîne un retard de prise en charge préjudiciable à la réputation de la marque.

## Données nécessaires et leur origine (obligatoire)
Un corpus historique d'avis clients négatifs collectés sur les plateformes en ligne, annotés et étiquetés selon leur degré d'urgence ou d'impact opérationnel par les équipes de gestion.

## Métrique de succès et seuil d'acceptation (obligatoire)
Un score F1 (F1-score) supérieur à 85 % sur la classe des avis critiques, garantissant un taux de faux négatifs suffisamment faible pour ne pas rater les urgences.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Un faux négatif retarde la résolution d'un problème client sensible, tandis qu'un faux positif mobilise à tort un niveau de support supérieur. Le système propose une priorisation automatisée, mais la décision finale de traitement et la réponse au client restent sous le contrôle d'un opérateur humain.

## Risques éthiques ou de confidentialité (obligatoire)
Présence potentielle de données personnelles identifiables (noms, coordonnées, numéros de commande) dans les textes des avis, nécessitant un nettoyage et une conformité stricte au RGPD.

## Approche écartée et pourquoi (facultatif)
L'approche par règles métier a été écartée car les formulations des clients sont trop diverses, variables et nuancées pour être capturées efficacement par des listes de mots-clés rigides.
