Objectif : créer un package qui génère automatiquement un package de ML 
Consignes du Readme : 
	- Expliquer comment est construit le code (dans les grandes lignes)
	- Etapes détaillées de la mise en production

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
            - setup.py (transforme la librairie en package). Ne pas supprimer. Utilise la bibliothèque setuptools. 
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

3. Ecrire tout le code dans un notebook. Le notebook doit être placé au même niveau que le package installé dans setup.py.
4. Factoriser et organiser le code en implémentant les fonctions créées dans les classes (fichiers.py)
5. Tester le code, avec notamment ipython dans le Terminal. Pour importer les modules créés, on doit se trouver dans le bon sous-dossier. 
        ipython
		from pkg_model_ml import ml

# Créer l'API avec FastAPI et uvicorn

1. Installer FastAPI et uvicorn
2. Créer un fichier main.py : importer les bibliothèques, créer les roots avec la méthode .get
3. Dans notre cas, nous avons : 
	- une prédiction qui retourne un résultat (en faisant appel à l'une de nos classes)
	- des graphiques qui retournent une JSONResponse.... COMPLETER
4. Faire tourner le serveur en local avec uvicorn : uvicorn nomdufichierdelapi:nomdudossier --reload
	ex : uvicorn main:app --reload
	Ne pas oublier de relancer cette commande dès qu'on apporte des modifications au fichier main.py
5. Pour consulter sur l'API : http://127.0.0.1:8000
	Pour accéder à la documentation : http://127.0.0.1:8000/docs


# Faire le lien entre l'API et une interface front (HTML/CSS/JavaScript)

# Docker : create image/container in localhost 

1. Créer le fichier Dockerfile, qui va donner les instructions à Docker pour construire l'image du container
2. Installer Docker si ce n'est pas déjà fait. Sur Windows, les pré-requis : .NET Framework à jour, WSL2 et Virtualisation activée.
3. Créer l'image à partir du fichier Dockerfile 
    docker build -t nom_de_l_image . # ne pas oublier le point à la fin (si mise en prod avec Azure, appeler le fichier du même nom que le container créé sur Azure)
	ex : docker build -t python-fastapi .
4. Exécute l'image en local / -d permet l'exécution du container en arrière-plan / -p permet de mapper un port arbitraire sur votre ordinateur vers le port 80 du conteneur
    docker run -p 8080:8000 python-fastapi

Notes : pour supprimer une image, vérifier qu'elle n'est utilisée par aucun container (manip depuis l'appli Docker Desktop ou docker rm/docker rmi)

# Mise en ligne de notre bibliothèque 
1. mettre un setup.py dans le package
2. Compilation/création du package : python setup.py sdist bdist_wheel
	Les dossiers build / dist apparaissent 
3. Pour publier le package et que les utilisateurs puissent le télécharger via un pip install : 
	- installer PyPi + compte utilisateur + twine
	- twine upload dist/*
4. On héberge notre package en ligne (ici sur Github). Le nom du repository doit être celui du "name" dans setup.py
5. Vérifier : pip install nomdelabibliotheque + lancer ipython : from nomdelabibliotheque import *


Notes : 
- Pour tester, il suffit de changer le n° de version dans le fichier setup.py et supprimer l'ancienne version téléchargée (pip uninstall nomdupackage).
- Ajouterle nom de notre bibliothèque dans requirements.txt


# Mise en production avec Azure : create a web app resource that can host the application

1. Activer son compte sur https://portal.azure.com/#home
2. Créer un Azure Container Registry (ACR) qui va stocker le container/image déjà créé avec Docker
	-> Aller sur Create a new resource -> Containers -> Container Registry (le nom donné doit être unique dans Azure)
3. Enovyer l'image créée avec Docker vers ACR :
	-> Aller sur le Container registry (titanicpackagegna) and récupérer le Login server in Access keys (Admin user must be "Enabled")
	-> Se connecter au registre : docker login nameofLoginServer and indicate password
		/!\ si on veut utiliser l'invite de commande Ubuntu, dans Docker Desktop, veiller à ce que les options suivantes soient cochées : General -> "Expose daemon on..." + Resources -> "WSL integration" -> Ubuntu
	-> Create a new image with the url of Azure created by container registry
	  This command will tell Docker to build your image using the Dockerfile in the current directory. It will also tag your image with your ACR repository name, an image name, and version set to latest to indicate that this image is the current version of the application.
		docker built -t Login_server/nom_que_l_on_veut_donner_a_l_image:latest .
		ex :  docker build -t titanicpackagegna.azurecr.io/package_titanic:latest .
	- Pushing the Image to ACR : 
		docker push <Login_server>/nom_image:latest .
4. Déployer sur Web App d'Azure
		

		
# Mise en ligne du front avec Githubpages

	




