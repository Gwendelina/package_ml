**Objectif** : conception d'une api qui utilise du machine learning (prédiction du Titanic)

Etapes du projet :

    1. Générer un template de projet (avec script exécutable)
    2. Créer un projet ML simple
    3. Créer l’API 
    4. Créer un container docker 
    5. Déployer le projet ML en production 
    6. Créer et utiliser une interface Front-end simple qui consomme l’API 


** EN LOCAL **

# Générer l'architecture et les dépendances

1. Ecrire le script qui génère automatiquement l'architecture de notre package :

	-> créer les dossiers et fichiers avec le module python os/ mkdir - touch	
	-> implémenter du code dans les fichiers standards en créant une fonction avec les méthodes open et write ayant pour paramètre un dictionnaire (clé : le nom du fichier, valeur : le code) : 
		- fichier de configuration **Makefile** (permet d'exécuter les actions indiquées quand on run le package) // actuellement remplacé par Dockerfile
			install_requirements:
				@pip install -r requirements.txt
			test:
				@run -m unittest tests/*.py
		- fichier **requirements.txt** (contient liste de commandes pour pip qui installe les versions requises des dépendances)
			soit les écrire manuellement
			soit 	py -m pip freeze > requirements.txt
					py -m pip install -r requirements.txt (privilégier la méthode manuelle)
		- fichier **setup.py** (transforme la librairie en package)
			from setuptools import setup
				setup(
					name='pkg_model_ml', # choisir le nom que l'on souhaite
					version='0.0.1', # version actuelle du modèle - peut être automatisé avec module Incremental
					packages=['titanicpackagegna'], # indiquer le nom du dossier qui contient le __init__
                    )
        - shutil.move("creation_architecture.py", "scripts/creation_architecture.py") -> afin que le fichier script soit dans le bon dossier 
		
2. Exécuter le script : python creation_architecture.py => l'architecture se génère

Notes : 
	- à chaque modification du package, il faut taper la commande *pip install .* OU installer le module qui permet d'initialiser automatiquement le package :
			*pip install -e .*       
			%load_ext autoreload
			%autoreload 2


# Créer le modèle de Machine Learning

1. Prépration d'un notebook de test (dossier notebooks)

2. Création des modules dans le package :
	- get_data.py : récupérer les données
	- preprocessing.py : inputer, encoding
	- model.py : sélectionne les features, split, prédiction, return_json_prediction (retourne prédiction au format json)
	- response_json.py : fonctions de data visualisation (qui seront appelées dans l'api)
	- controler.py : exécute le modèle et ses résultats
	
3. Tester le fonctionnement des classes et des imports avec Ipython :
        ipython
		from pkg_model_ml import ml
		


# Créer l'API avec FastAPI et uvicorn

1. Installer FastAPI et uvicorn

2. Créer un fichier main.py : importer les bibliothèques, créer l'objet de FastApi, créer les roots avec la méthode .get

3. Dans notre cas, l'api permet de : 
	- d'afficher le résultat d'une prédiction appelé depuis le controler.py 
	- de retourner des résultats de visualisation sous format json (module JSONResponse)
	
4. Faire tourner le serveur en local avec uvicorn : **uvicorn nomdufichierdelapi:nomdelinstance --reload**
	ex : uvicorn main:app --reload
	Ne pas oublier de relancer cette commande dès qu'on apporte des modifications au fichier main.py
	
5. Pour consulter l'API : http://127.0.0.1:8000 / Pour accéder à la documentation : http://127.0.0.1:8000/docs


# Créer l'interface front avec HTML, CSS et JavaScript
	
	- Le front (Javascript) récupère les réponses json de l'api: 
		- indiquer l'url du localhost de l'api depuis laquelle on récupère les données (dans graph.js)
		- pour chaque graphique, utiliser la méthode de JavaScript "Highcharts.getJSON" qui permet d'accéder à chaque root de l'api 
		- puis mapper (pointer) sur le résultat des fonctions de visualisation pour les transformer en graph 
			
			const url = "http://127.0.0.1:8000"

			Highcharts.getJSON(url + "sex_survived",
				function (data) {
				const platform = data.map(d => [d.name,  d.pourcent]);
		
	- Pour tester en local la page, lancer le fichier index.html
	

# Création d'une image/container avec Docker en local

Notre container contient l'api et notre package (modèle ML) 
	=> transfert du dossier package sous le dossier app_container
	=> transfert du fichier requirements.txt dans le dossier app_container

1. Installer Docker Dekstop. Avec Windows, les pré-requis sont : .NET Framework à jour, WSL2, Ubuntu et virtualisation activée.

2. Créer le fichier Dockerfile, qui va donner les instructions à Docker pour construire l'image du container:
	- FROM : doit être la 1ère instruction du Dockerfile. Constitue la base de l'image (définit le langage et le système d'exploitation)
	- RUN : exécute l'installation des dépendances nécessaires au fonctionnement de l'image 
	- COPY : récupère les dossiers/fichiers dont on a besoin pour constituer l'image et les ajoute dans l'image
	- EXPOSE : port écouté par le container
	- CMD : définit la commande par défaut qui va s'executer au démarrage du container. Ici, lancement de guvicorn via un fichier de config.py qui permet de lancer l'image sur un serveur web/local ?

3. Créer l'image : **docker build -t nom_de_l_image/ .**
     /!\ ne pas oublier le point à la fin 
	 /!\ si mise en prod avec Azure, appeler l'image du même nom que le container créé sur Azure (Login Server)
	 
4. Exécute l'image en local : **docker run -p 8080:8000 nom_de_l_image**
	-d permet l'exécution du container en arrière-plan
	-p permet de mapper un port arbitraire sur votre ordinateur vers le port 80 du conteneur
    

Notes : 
	- pour visualiser/supprimer les images et les containers, utiliser l'appli Docker Desktop
	- pour supprimer une image, vérifier qu'elle n'est utilisée par aucun container (manip depuis l'appli Docker Desktop ou docker rm/docker rmi)




** MISE EN PRODUCTION **

# Mise en production de l'api avec Azure

![alt text](http:https://cdn.discordapp.com/attachments/836540967272185866/877474484393738270/schema_ACR.png//url/to/img.png)

1. Activer son compte sur https://portal.azure.com/#home

2. Créer un Azure Container Registry (ACR) qui va stocker le container/image déjà créé avec Docker
	-> Aller sur Create a new resource -> Containers -> Container Registry (le Registry name donné doit être unique dans Azure)
	
3. Envoyer l'image créée avec Docker vers l'ACR :
	-> Aller sur le Container registry (titanicpackagegna) and récupérer le Login server dans Access keys (Admin user must be "Enabled")
	-> Se connecter au registre via le Terminal : **docker login name_of_LoginServer** and indicate password
		/!\ si on veut utiliser l'invite de commande Ubuntu, dans Docker Desktop, veiller à ce que les options suivantes soient cochées : General -> "Expose daemon on..." + Resources -> "WSL integration" -> Ubuntu
	-> Pusher l'image dans l'ACR : **docker push nom_image/app_api**
	   *le latest se génère automatiquement (indique que l'image est la version actuelle)
	   *app_api correspond au nom qu'on donne au dossier repository dans lequel sera hébergé notre image.
		 -> pour vérifier : aller sur son container registry -> Repositories -> tous ceux créés pour ce container apparaissent.
		 
4. Déployer l'image disponible dans l'ACR via Web App
	-> Create Web App 
		-> dans l'onglet Basics :
			* Publish -> Docker Container
			* Operating System -> Linux
			* Sku and size -> 1 Go
		-> dans l'onglet Docker :
			* Image Source : Azure Container Registry
			* Image : choisir le nom du repository dans lequel se situe votre image
	-> Dans Home, ouvrir l'onglet de l'App service, la run et cliquer sur l'url 	

Notes : 
	- la Web app ne fonctionnait pas quand on utilisait uvicorn dans notre fichier Dockerfile (CMD qui renvoyait vers le fichier main.py de l'api *uvicorn.run(app, host="0.0.0.0", port=8000))
	- Pour faire en sorte que la page web soit mise à jour en cas de changement d'image, possibilité d'activer le "continuous deployement" 	
	
# Mise en production du front avec Githubpages

1. Dans le fichier graph.js, changer l'url de l'api par celle mise en production avec Azure : 
	-> const url = "https://titanicapi.azurewebsites.net/"
2. Créer un repository Github sur lequel on ne dépose que les dossiers du front
	-> le nommer ainsi : nom_du_repo.github.io
	-> dans Settings -> Pages -> changer la source, et le lien de publication apparaît

	


** OPTIONNEL **

# Mise en ligne de notre bibliothèque 

1. Mettre un setup.py dans le package
2. Compilation/création du package : **python setup.py sdist bdist_wheel** (les métadonnées build / dist se génèrent)
3. Pour publier le package et que les utilisateurs puissent le télécharger via un pip install : 
	- installer PyPi + créer un compte utilisateur + installer twine
	- dans le Terminal : **twine upload dist/* ***
4. On héberge notre package en ligne (ici sur Github). Le nom du repository doit être celui du "name" dans setup.py
5. Vérifier : pip install nomdelabibliotheque + lancer ipython : from nomdelabibliotheque import *


Notes : 
	- Pour tester, il suffit de changer le n° de version dans le fichier setup.py et supprimer l'ancienne version téléchargée (pip uninstall nomdupackage).
	- Ajouter le nom de notre bibliothèque dans requirements.txt
	- A creuser : abandon de la mise en ligne de la bibliothèque car dans l'api, on ne parvenait pas à stocker le résultat d'une variable nécessaire à l'une de nos viz, lors du déploiement avec Azure. 




