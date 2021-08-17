import sys
from fastapi import FastAPI
import uvicorn
from titanicpackagegna.response_json import Response_json
import warnings
warnings.filterwarnings("ignore")
from fastapi.responses import JSONResponse
from titanicpackagegna.controler import controler


model, ml, X, y = controler()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bienvenue sur notre API"}


@app.get("/prediction/pclass={pclass}/sex={sex}/age={age}/sibsp={sibsp}/parch={parch}/fare={fare}/embarked={embarked}")
async def prediction(pclass, sex, age, sibsp, parch, fare, embarked): 
    return ml.prediction(model, int(pclass), int(sex), int(age), int(sibsp), int(parch), float(fare), int(embarked))


@app.get("/count_predictions")
async def count_predictions():
    return JSONResponse(content=ml.return_json_prediction(), headers= {"Access-Control-Allow-Origin":"*"})

@app.get("/sex_survived")
async def sex_survived():
    return JSONResponse(content=Response_json().sex_survived(X,y), headers= {"Access-Control-Allow-Origin":"*"})


@app.get("/pclass_survived")
async def pclass_survived():
    return JSONResponse(content=Response_json().pclass_survived(X,y), headers= {"Access-Control-Allow-Origin":"*"})

@app.get("/age_survived")
async def age_survived():
    return JSONResponse(content=Response_json().age_survived(X,y), headers= {"Access-Control-Allow-Origin":"*"})


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)