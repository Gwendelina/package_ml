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
    return ml.prediction(model, int(pclass), int(sex), int(age), int(sibsp), int(parch), float(fare), int(embarked))


@app.get("/count_predictions")
async def count_predictions():
    return JSONResponse(content=ml.return_json_prediction(), headers= {"Access-Control-Allow-Origin":"*"})

@app.get("/sex_survived")
async def sex_survived():
    # transforme le dico en json
    # autorise l'extérieur à récupérer les données de l'API
    return JSONResponse(content=Response_json().sex_survived(X,y), headers= {"Access-Control-Allow-Origin":"*"})


@app.get("/pclass_survived")
async def pclass_survived():
    return JSONResponse(content=Response_json().pclass_survived(X,y), headers= {"Access-Control-Allow-Origin":"*"})

@app.get("/age_survived")
async def age_survived():
    return JSONResponse(content=Response_json().age_survived(X,y), headers= {"Access-Control-Allow-Origin":"*"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)