## Activation API Google Maps
Utilisée dans la mobility_map pour afficher des photos des universités, et une intégration StreetView.

1. Allez sur [Google Cloud Console](https://console.cloud.google.com/).
2. Créez un projet ou sélectionnez-en un existant.
3. Accédez à "APIs & Services".
4. activez les API suivantes :
    - Places API
    - Geocoding API
5. Copiez la clé API générée.
6. Ajoutez dans le .env : GOOGLE_MAPS_API_KEY=votre_clé_api
7. Redémarrez l'application pour que les changements prennent effet.