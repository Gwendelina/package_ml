Objectif : créer un package qui génère automatiquement un package de ML (voir projet "package_titanic_final)

Etapes du projet :

    1. Générer un template de projet (avec script exécutable)
    2. Créer un projet ML simple
    3. Créer l’API 
    4. Créer un container docker 
    5. Déployer le projet ML en production 
    6. Créer et utiliser une interface Front-end simple qui consomme l’API 

# Installer et configurer l'architecture et les dépendances

1. Ecrire le script qui génère automatiquement les dossiers et les fichiers relatifs à l'architecture du package:

        - créer les dossiers et fichiers avec le module python os/mkdir.touch
        - implémenter du code dans les fichiers standards en créant une fonction avec les méthodes open et write ayant pour paramètre un dictionnaire (clé : le nom du fichier, valeur : le code) : 
            - fichier Makefile (génère automatiquement des tâches - REVOIR UTILITE)
                install_requirements:
                    @pip install -r requirements.txt
                test:
                    @run -m unittest tests/*.py
            - fichier requirements.txt (contient liste de commandes pour pip qui installe les versions requises des dépendances). 
                soit les écrire manuellement
                soit 	py -m pip freeze > requirements.txt
                        py -m pip install -r requirements.txt (d'après lecture, à manipuler avec précaution - A VERIFIER)
            - setup.py (transforme la librairie en package). Utilise la bibliothèque setuptools. 
                from setuptools import setup
                    setup(
                        name='pkg_model_ml', # choisir le nom que l'on souhaite
                        version='0.0.1', # peut être automatiser avec module Incremental
                        packages=['pkg_model_ml'], # indiquer le nom du dossier qui contient le __init__
                        # scripts = ['scripts/display'] # VOIR A QUI CELA SERT - DU COUP, NE PAS FAIRE LE SHUTIL.MOVE
                    )
            - on peut ajouter aussi le fichier gitignore (mais pas testé)
        - os.system -> exécuter les requirements depuis le Makefile (make .... RETROUVER LE CODE)
        - shutil.move("creation_architecture_test.py", "scripts/creation_architecture_test.py") -> afin que le fichier script soit dans le bon dossier 
        - Quand le code est terminé, lancer le fichier script dans un terminal Python => l'architecture se génère

2. Tester le pip install . du package afin de confirmer que tout est ok. A chaque modification il faudra :

        - soit refaire la manip pip install .
        - soit  pip install -e .       => permet au package de s'initialiser automatiquement
                %load_ext autoreload
                %autoreload 2


# Créer le modèle de Machine Learning

3. Ecrire tout le code dans un Jupyter
4. Factoriser et organiser le code en implémentant les fonctions créees dans les classes (fichiers.py)
5. Tester le code, avec notamment ipython dans le Terminal. Pour importer les modules créés, on doit se trouver dans le bon sous-dossier. 
        ipython
		from pkg_model_ml import ml

# Créer l'API

Va servir à stocker les résultats de la prédiction par exemple ou le code des graphiques qu'on va vouloir partager avec l'utilisateur - PRECISER
Utilisation de FastAPI et Uvicorn

# Faire le lien entre l'API et une interface front (HTML/CSS/JavaScript)

# Docker

1. Ne pas oublier de créer le Dockerfile.
2. Créer l'image
    docker build -t python fastapi-app .

