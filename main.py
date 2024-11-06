from sensor.configuration.mongodb_db_connection import MongoDBClient
from sensor.exception import SensorException
import os, sys
from sensor.logger import logging
from sensor.pipeline.traning_pipeline import TrainPipeline
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from uvicorn import run as app_run
from sensor.ml.model.estimator import ModelResolver
import pandas as pd
from sensor.constant.application import APP_HOST, APP_PORT


app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train", tags=["training"])
async def train():
    try:
        training_pipeline = TrainPipeline()
        if training_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        
        training_pipeline.run_pipeline()
        return Response("Training successfully completed!")
    except Exception as e:
        logging.exception("Training failed")
        return Response(content=f"Error Occurred! {e}", status_code=500)

@app.post("/predict", tags=["prediction"])
async def predict(file: UploadFile = File(...)):
    try:
        model_resolver = ModelResolver()
        model = model_resolver.get_model()
        data = pd.read_csv(file.file)
        predictions = model.predict(data)
        return {"predictions": predictions.tolist()}
    except Exception as e:
        logging.exception("Prediction failed")
        return Response(content=f"Error Occurred! {e}", status_code=500)


# def main():
#     try:
#         training_pipeline = TrainPipeline()
#         training_pipeline.run_pipeline()

#     except Exception as e :
#         print(e)
#         logging.exception(e)



def test_exception():
    try:
        logging.info("Error present!") # No uppercase of info
        a=1/0
    except Exception as e:
        raise SensorException(e,sys)



if __name__=='__main__':
    # try:
    #     test_exception()
    # except Exception as e:
    #     print(e)

    # file_path="/Bakchodi/LiveSensor/LiveSensor_FULL_MLProject/aps_failure_training_set1.csv"
    # database_name="liveSensorDB"
    # collection_name ="sensorCollection"
    # dump_csv_file_to_mongodb_collection(file_path,database_name,collection_name)

    app_run(app, host=APP_HOST, port=APP_PORT)  # Replace with APP_HOST and APP_PORT as needed


