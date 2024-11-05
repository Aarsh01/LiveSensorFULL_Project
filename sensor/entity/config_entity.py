from datetime import datetime
import os
from sensor.constant import training_pipeline


# This class is made to build the folder(1, 2, 3) on different timestamp after the artifact folder is builded....
class TrainingPipelineConfig:
   
    def __init__(self,timestamp=datetime.now()):

        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")  # Example format: '20231021_153000'

        self.pipeline_name: str = training_pipeline.PIPELINE_NAME  # This is a pipeline, so name it, according to below fig.

        self.artifact_dir: str = os.path.join(training_pipeline.ARTIFACT_DIR, timestamp)  # timestamp folder is in artifacts diratory 

        self.timestamp: str = timestamp
        
    # According to below fig, (a to b) or (b in a) is build


# Example: If training_pipeline.ARTIFACT_DIR is /path/to/artifacts and timestamp is 10_20_2024_15_30_00, 
# then self.artifact_dir would be /path/to/artifacts/10_20_2024_15_30_00.

############ Hence till b-part has build!. ######################

"""
There are 6 parts ...............

                        From fig-0 from flowcharts: 1st Part 
MongoDB Database + Data Ingestion Config ---> Data Ingestion Component -----> Data Ingestion Artifacts
"""

# 1st Part 
"""
        artifacts (a)
            |
            |              
            v                     
        timestampt (b)-------------- --------------------------|
            |                       |                          |
            |                       |                          |
            v   (1)                 v    (2)                   v  (3)
        DATA INGESTION         DATA VALIDATION           DATA TRANSFORMATION                                           
            |       |                                                          
            |       |-----------|                                                          
            v                   |                                                
        ingested_data-----|     |------> Feature Store  
            |             |                 |
            |             |                 |
            v             v                 v
        train.csv      test.csv          sensor.csv  <--------------- MogoDb

"""


# # ***************** 1 **********************

class DataIngestionConfig: 
       
        # Basically We are setting the path of the folders according to the above fig provided.
        # Take the help of the above fig and variables from 'training_pipeline' from sensor.training_pipeline.py

        def __init__(self,training_pipeline_config:TrainingPipelineConfig):

            self.data_ingestion_dir: str = os.path.join(
                training_pipeline_config.artifact_dir, 
                training_pipeline.DATA_INGESTION_DIR_NAME
            )
            # Example: If artifact_dir is /path/to/artifacts/10_20_2024_15_30_00 and DATA_INGESTION_DIR_NAME is data_ingestion, 
            # then self.data_ingestion_dir would be /path/to/artifacts/10_20_2024_15_30_00/data_ingestion.

            ######## Hence (b to 1) or (1 in b) is done! ########

            self.feature_store_file_path: str = os.path.join(
                self.data_ingestion_dir, 
                training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, 
                training_pipeline.FILE_NAME
            )
            # Example: If data_ingestion_dir is /path/to/artifacts/10_20_2024_15_30_00/data_ingestion, 
            # DATA_INGESTION_FEATURE_STORE_DIR is feature_store, 
            # and FILE_NAME is features.csv, 
            # then self.feature_store_file_path would be /path/to/artifacts/10_20_2024_15_30_00/data_ingestion/feature_store/features.csv.



            self.training_file_path: str = os.path.join(
                self.data_ingestion_dir, 
                training_pipeline.DATA_INGESTION_INGESTED_DIR, 
                training_pipeline.TRAIN_FILE_NAME
            )

            self.testing_file_path: str = os.path.join(
                self.data_ingestion_dir, 
                training_pipeline.DATA_INGESTION_INGESTED_DIR, 
                training_pipeline.TEST_FILE_NAME
            )
            #Example: If DATA_INGESTION_INGESTED_DIR is ingested_data, 
            # TRAIN_FILE_NAME is train.csv, and TEST_FILE_NAME is test.csv, then:
            # self.training_file_path would be /path/to/artifacts/10_20_2024_15_30_00/data_ingestion/ingested_data/train.csv.
            # self.testing_file_path would be /path/to/artifacts/10_20_2024_15_30_00/data_ingestion/ingested_data/test.csv.
            

            self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
            self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME

# Example usage
"""
if __name__ == "__main__":
    current_timestamp = datetime.now()  # Replace with your actual timestamp logic
    training_pipeline_config = TrainingPipelineConfig(timestamp=current_timestamp)
    print(training_pipeline_config.artifact_dir)  # Just for verification
"""

# ********************************* NEXT STEP *********************************
# *********************************   STEP    *********************************
# ********************************* NEXT STEP *********************************
# *********************************   STEP    *********************************



"""
                           From fig-0 from flowcharts: 2nd Part 
Data Ingestion Component + Data Ingestion Artifacts + Data Validation Config ---> Data Validation Component -----> Data Validation Artifacts
                                                                                            |--------------------> Data Tranformation Component

"""                 

"""
constant ----> Entity ---------|
                |              |
                |              |
                |              |
                v              v
            config         artifact
              of              of 
            component      component
               |              |
               |              |
               |_______|______|
                       |
                       |
                       v
         |--------> Component --------> trainPipeline ------> validation artifact
 ________|____________
| ingestion artifact |
| validation config  |
| schema file data   |
|____________________|            

"""

# # ***************** 2 **********************

class DataValidationConfig:
     def __init__(self, training_pipeline_config:TrainingPipelineConfig):

        # from (b to 2) or (2 in b) in Fig-0 of 1st part
        self.data_validation_dir: str = os.path.join( 
            training_pipeline_config.artifact_dir, 
            training_pipeline.DATA_VALIDATION_DIR_NAME
        ) # Result: /path/to/artifacts/10_20_2024_15_30_00/data_validation


        self.valid_data_dir: str = os.path.join(
            self.data_validation_dir, 
            training_pipeline.DATA_VALIDATION_VALID_DIR
        ) # Result: /path/to/artifacts/10_20_2024_15_30_00/data_validation/valid

        
        self.invalid_data_dir: str = os.path.join(
            self.data_validation_dir, 
            training_pipeline.DATA_VALIDATION_INVALID_DIR
        ) # Result: /path/to/artifacts/10_20_2024_15_30_00/data_validation/invalid


        self.valid_train_file_path: str = os.path.join(
            self.valid_data_dir, 
            training_pipeline.TRAIN_FILE_NAME
        ) # Result: /path/to/artifacts/10_20_2024_15_30_00/data_validation/valid/train.csv


        self.valid_test_file_path: str = os.path.join(
            self.valid_data_dir, 
            training_pipeline.TEST_FILE_NAME
        ) # Result: /path/to/artifacts/10_20_2024_15_30_00/data_validation/valid/test.csv


        self.invalid_train_file_path: str = os.path.join(
            self.invalid_data_dir, 
            training_pipeline.TRAIN_FILE_NAME
        ) # Result: /path/to/artifacts/10_20_2024_15_30_00/data_validation/invalid/train.csv


        self.invalid_test_file_path: str = os.path.join(
            self.invalid_data_dir, 
            training_pipeline.TEST_FILE_NAME
        ) # Result: /path/to/artifacts/10_20_2024_15_30_00/data_validation/invalid/test.csv

        
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        ) # Result: /path/to/artifacts/10_20_2024_15_30_00/data_validation/drift_report/report.csv


# ********************************* NEXT STEP *********************************
# *********************************   STEP    *********************************
# ********************************* NEXT STEP *********************************
# *********************************   STEP    *********************************

"""
                                    ____________________
      Config  ------------|        |                    |       |---------> Processed Object -->(preprocessed.pkl file)
                          |        |                    |       |
                          |------> |  TRANSFORMATION    |-------|
                          |        |                    |       |
    Artifact -------------|        |____________________|       |---------> transformed --> train.npy and test.npy
        |                                    |
    ____|___                                 |
   |        |                                v
   |        |                               EDA
   v        v
Train.csv Test.csv



"""
# # ***************** 3 **********************
class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):


        self.data_transformation_dir: str = os.path.join( 
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_TRANSFORMATION_DIR_NAME 
        )
        
        self.transformed_train_file_path: str = os.path.join( 
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),
        )
        
        self.transformed_test_file_path: str = os.path.join(
            self.data_transformation_dir,  
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy"), 
        )
        
        self.transformed_object_file_path: str = os.path.join( 
            self.data_transformation_dir, 
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCSSING_OBJECT_FILE_NAME,
        )
"""
LiveSensor_FULL_MLProject/
│
├── artifacts/
│   └── data_transformation/
│       ├── transformed_data/
│       │   ├── train.npy
│       │   └── test.npy
│       └── preprocessing_object.pkl
"""
   

# ********************************* NEXT STEP *********************************
# *********************************   STEP    *********************************
# ********************************* NEXT STEP *********************************
# *********************************   STEP    *********************************

# """
# """

# # ***************** 4 **********************
class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINER_DIR_NAME
        )

        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR, 
            training_pipeline.MODEL_FILE_NAME
        )
        self.expected_accuracy: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold = training_pipeline.MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD


# ********************************* NEXT STEP *********************************
# *********************************   STEP    *********************************
# ********************************* NEXT STEP *********************************
# *********************************   STEP    *********************************


# # ***************** 5 **********************
class ModelEvaluationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):

        self.model_evaluation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.MODEL_EVALUATION_DIR_NAME
        )
        self.report_file_path = os.path.join(self.model_evaluation_dir,training_pipeline.MODEL_EVALUATION_REPORT_NAME       )
        
        self.change_threshold = training_pipeline.MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE


# ********************************* NEXT STEP *********************************
# *********************************   STEP    *********************************
# ********************************* NEXT STEP *********************************
# *********************************   STEP    *********************************


# # ***************** 6 **********************
class ModelPusherConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):

        self.model_evaluation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.MODEL_PUSHER_DIR_NAME
        )

        self.model_file_path = os.path.join(self.model_evaluation_dir,training_pipeline.MODEL_FILE_NAME)
        
        timestamp = round(datetime.now().timestamp())

        self.saved_model_path=os.path.join(
            training_pipeline.SAVED_MODEL_DIR,
            f"{timestamp}",
            training_pipeline.MODEL_FILE_NAME)