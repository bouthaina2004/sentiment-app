# Déployer l'interface Streamlit

L'interface peut utiliser l'API en mode local (`SENTIMENT_BACKEND = "api"`) ou
le modèle inclus dans le paquet publié (`SENTIMENT_BACKEND = "package"`). Le
second mode convient à Streamlit Community Cloud : son `localhost` n'est pas
celui de votre ordinateur et ne peut donc pas joindre votre API locale.

## Préparer la release du paquet

La dépendance [ui/requirements.txt](../ui/requirements.txt) installe le wheel
de la release `v1.0.1`. Il faut d'abord publier cette release GitHub avec les
deux distributions construites (`dist/sentiment_app-1.0.1-py3-none-any.whl` et
`dist/sentiment_app-1.0.1.tar.gz`).

## Créer l'application distante

1. Sur Streamlit Community Cloud, créez une application à partir du dépôt
   `bouthaina2004/sentiment-app`, branche `main`, fichier d'entrée `ui/app.py`.
2. Dans les paramètres **Secrets**, ajoutez :

   ```toml
   SENTIMENT_BACKEND = "package"
   ```

3. Relancez l'application et vérifiez que la page indique
   `modèle du paquet sentiment-app 1.0.1`.
4. Testez un avis positif, un négatif, un texte incertain, puis un CSV. Le
   seuil d'abstention reste fixé à 0,60. La page et le modèle s'exécutent alors
   dans l'environnement hébergé ; aucune API de votre ordinateur n'est requise.

L'application distante n'a pas encore été créée par ce dépôt : cette dernière
étape exige une connexion à votre compte Streamlit Community Cloud. La clé
`API_KEY` n'est pas nécessaire en mode paquet.
