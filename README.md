
Générateur de Cours et Exercices

Une application Python avec une interface graphique permettant de générer automatiquement des cours structurés et des exercices associés grâce à l'API Claude.

Fonctionnalités
---------------
- Génération de cours :
  - Entrez un sujet, un niveau, et une durée pour générer un cours structuré.
  - Chaque cours inclut des titres, descriptions, et objectifs pédagogiques.

- Génération d'exercices :
  - Créez des exercices basés sur le cours généré, incluant :
    - QCM
    - Questions ouvertes
    - Exercices pratiques

- Sauvegarde automatique et manuelle :
  - Sauvegardez les cours et exercices générés au format JSON dans le dossier `cours_exercices`.

- Récupération des cours sauvegardés :
  - Affichez la liste des fichiers JSON disponibles dans le dossier.
  - Importez un cours et ses exercices à partir de cette liste.

- Interface intuitive :
  - Interface utilisateur développée avec `tkinter` pour une utilisation simple et rapide.

Prérequis
---------
Environnement Python
- Version minimale : Python 3.7 ou plus récent
- Modules requis : requests (à installer si nécessaire)

Installez requests avec :
pip install requests

Clé API Claude
1. Créez un compte sur Anthropic et récupérez une clé API valide.
2. Remplacez la valeur de `API_KEY` dans le script par votre propre clé.

Installation
------------
1. Clonez ce projet ou téléchargez les fichiers nécessaires :
   git clone https://github.com/richard-lam-webdev/tp-ia-generation-cours.git
   cd votre-repo

2. Assurez-vous d'avoir un environnement Python correctement configuré.
3. Installez les dépendances nécessaires.

Utilisation
-----------
1. Exécutez l'application :
   python main.py

2. Générez un cours :
   - Remplissez les champs "Sujet", "Niveau" et "Durée".
   - Cliquez sur "Générer le cours".

3. Générez des exercices :
   - Après avoir généré un cours, cliquez sur "Générer les exercices".

4. Enregistrez les cours et exercices :
   - Cliquez sur "Enregistrer Cours/Exercices" pour sauvegarder les contenus générés dans le dossier `cours_exercices`.

5. Récupérez un cours existant :
   - Sélectionnez un fichier dans la liste des cours disponibles.
   - Cliquez sur "Récupérer le cours/exercices" pour afficher son contenu.

Structure de Projet
-------------------
├── main.py               # Fichier principal de l'application
├── cours_exercices/      # Dossier contenant les fichiers JSON générés
├── README.md             # Documentation du projet

Exemple de Fichier JSON Généré
------------------------------
{
    "course": "Contenu structuré du cours généré...",
    "exercises": "Exercices associés générés à partir du cours..."
}

Licence
-------
Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus de détails.
