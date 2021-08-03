# permet d'interagir avec le système d'exploitation
import os 

# redéfinir le nom des fichiers en fonction du projet actuel
def creation_architecture(project_name):
    os.system(f"mkdir {project_name}")
    os.system(f"touch {project_name}/__init__.py")
    os.system(f"touch {project_name}/preprocessing.py")
    os.system(f"touch {project_name}/pipeline.py")
    os.system(f"touch {project_name}/get_data.py")
    os.system(f"touch {project_name}/model.py")
    os.system(f"touch setup.py")
    os.system(f"mkdir notebooks")
    os.system(f"mkdir api")
    os.system(f"mkdir data")
    os.system(f"mkdir tests")
    os.system(f"touch api/fast.py")
    os.system(f"touch README.md")
    os.system(f"touch requirements.txt")
    os.system(f"touch Makefile")
    os.system(f"mkdir scripts")


creation_architecture('titanic')