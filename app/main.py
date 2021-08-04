import sys
# sys.path.append("..")
from fastapi import FastAPI
import uvicorn
from package_ml.get_data import Data
from package_ml.preprocessing import Preprocessing
from package_ml.model import Model
from package_ml.response_json import Response_json
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings("ignore")
from fastapi.responses import JSONResponse


do = Data('titanic') 
titanic_data = do.get_data()
preproc = Preprocessing(titanic_data)
preproc.drop('Cabin')
preproc.mean_inputer('Age')
preproc.mode_inputer('Embarked')
preproc.encoding('Sex','Embarked')
titanic_data = preproc.final_df()
ml = Model(titanic_data)
X = ml.X_features_drop(['PassengerId','Name','Ticket','Survived'])
y = ml.y_target(['Survived'])
X_train, X_test, y_train, y_test = ml.split(X,y,test_size=0.2,random_state=2)
model = LogisticRegression()
model.fit(X_train, y_train)
X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(y_train, X_train_prediction)
X_test_prediction = model.predict(X_test)
test_data_accuracy = accuracy_score(y_test, X_test_prediction)


app = FastAPI()
# uvicorn api:app --reload

@app.get("/")
async def root():
    return {"message": "ONLINE"}


@app.get("/prediction/pclass={pclass}/sex={sex}/age={age}/sibsp={sibsp}/parch={parch}/fare={fare}/embarked={embarked}")
async def prediction(pclass, sex, age, sibsp, parch, fare, embarked):
    # message = ""
    # error = False
    # if pclass != 1 or pclass != 2 or pclass != 3 or type(pclass) != int:
    #     message += "ERROR : La classe doit être 1, 2 ou 3.\n"
    #     error == True
    # if sex != 1 or sex != 0 or type(sex) != int:
    #     message += "ERROR : Le sexe doit être 0 ou 1. La valeur 0 correspond à un homme et 1 à une femme.\n"
    #     error == True
    # if age < 0 or age > 100 or type(age) != int:
    #     message += "ERROR : L'âge doit être compris entre 0 et 100.'\n"
    #     error == True
    # if sibsp < 0 or type(sibsp) != int:
    #     message += "ERROR : La variable sibsp doit contenir une valeur positive.\n"
    #     error == True
    # if parch < 0 or type(parch) != int:
    #     message += "ERROR : La variable parch doit contenir une valeur positive.\n"
    #     error == True
    # if fare < 0:
    #     message += "ERROR : Le prix du billet ne peut être inférieur à 0$.\n"
    #     error == True
    # if embarked != 0 or embarked != 1 or embarked != 2 or type(embarked) != int:
    #     message += "ERROR : Le port d'embarquement doit 0, 1 ou 2.\n"
    #     error == True
    # if error == True:
    #     return message
    # else:    
    return ml.prediction(model, int(pclass), int(sex), int(age), int(sibsp), int(parch), float(fare), int(embarked))



@app.get("/sex_survived")
async def sex_survived():
    # transforme le dico en json
    # autorise l'extérieur à récupérer les données de l'API
    return JSONResponse(content=Response_json().sex_survived(X,y), headers= {"Access-Control-Allow-Origin":"*"})


@app.get("/pclass_survived")
async def pclass_survived():
    # transforme le dico en json
    # autorise l'extérieur à récupérer les données de l'API
    return JSONResponse(content=Response_json().pclass_survived(X,y), headers= {"Access-Control-Allow-Origin":"*"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


