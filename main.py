from sensor.configuration.mongodb_db_connection import MongoDBClient
from sensor.exception import SensorException
import os , sys
from sensor.logger import logging
#from  sensor.utils import dump_csv_file_to_mongodb_collecton
#from sensor.entity.config_entity  import TrainingPipelineConfig,DataIngestionConfig

from sensor.pipeline.traning_pipeline import TrainPipeline

# def test_exception():
#     try:
#         logging.info("Error present!") # No uppercase of info
#         a=1/0
#     except Exception as e:
#         raise SensorException(e,sys)

if __name__=='__main__':
    # try:
    #     test_exception()
    # except Exception as e:
    #     print(e)

    # file_path="/Bakchodi/LiveSensor/LiveSensor_FULL_MLProject/aps_failure_training_set1.csv"
    # database_name="liveSensorDB"
    # collection_name ="sensorCollection"
    # dump_csv_file_to_mongodb_collection(file_path,database_name,collection_name)

    training_pipeline = TrainPipeline()
    training_pipeline.run_pipeline()
