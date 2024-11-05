## The class includes methods for validating columns, checking for numerical columns, and detecting dataset drift.
"""
Overview of DataValidation Class
Initialization: Accepts artifacts for data ingestion and configuration for data validation, and reads a schema file.

Column Validation:
validate_number_of_columns: Checks if the number of columns in the DataFrame matches the expected number defined in the schema.
is_numerical_column_exist:  Validates the presence of required numerical columns in the DataFrame.

Data Reading:
read_data: Static method to read CSV files into DataFrames.

Drift Detection:
detect_dataset_drift: Compares distributions of columns in training and testing datasets using the Kolmogorov-Smirnov test.

Validation Process:
initiate_data_validation: Orchestrates the validation process, checks for errors, and generates a drift report.
"""

from distutils import dir_util
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig

from sensor.exception import SensorException
from sensor.logger import logging

from sensor.utils.main_utils import read_yaml_file, write_yaml_file

from scipy.stats import ks_2samp # check the Data Drift
import pandas as pd
import os,sys


class DataValidation:

    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                        data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH) # Private variable

        except Exception as e:
            raise  SensorException(e,sys)
    """
    Purpose:
    1. Initialize the DataValidation object.
    2. Accepts artifacts for data ingestion and validation configuration.
    3. Reads the schema configuration from a YAML file, which contains the expected structure of the datasets.
    4. Raises an exception if any initialization fails, ensuring that the object is always in a valid state
    """
        
    def drop_zero_std_columns(self,dataframe):
        pass

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")

            if len(dataframe.columns)==number_of_columns:
                return True
            
            return False
        except Exception as e:
            raise SensorException(e,sys)
    """
    Purpose: 
    1. Validate the number of columns in a DataFrame.
    2. Compares the actual number of columns in the DataFrame to the expected number from the schema.
    3. Logs both values for transparency.
    4. Returns True if the counts match, ensuring that the dataset adheres to the expected structure. If not, it returns False.
    5. Raises an exception if an error occurs, which helps in debugging.
    """
    
    def is_numerical_column_exist(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = self._schema_config["numerical_columns"]
            dataframe_columns = dataframe.columns

            numerical_column_present = True
            missing_numerical_columns = []

            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_present=False
                    missing_numerical_columns.append(num_column)
            
            logging.info(f"Missing numerical columns: [{missing_numerical_columns}]")

            return numerical_column_present
        
        except Exception as e:
            raise SensorException(e,sys)
    """
    Purpose: 
    1. Check for the existence of required numerical columns.
    2. Retrieves the list of expected numerical columns from the schema.
    3. Initializes a flag to track the presence of numerical columns and a list for missing columns.
    4. Iterates through the expected numerical columns, checking if each one exists in the DataFrame.
    5. Logs any missing columns, which helps identify issues in the dataset.
    6. Returns True if all required numerical columns are present; otherwise, returns False.
    7. Raises an exception if an error occurs.
    """
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e,sys)
    """
    Purpose: 
    1. Read a CSV file and return it as a DataFrame.
    2. This static method simplifies the process of loading data, making it reusable across different parts of the class.
    3. Raises a SensorException if reading the file fails, ensuring that errors are handled properly.
    """

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report ={}
            for column in base_df.columns:
                d1 = base_df[column]
                d2  = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found = True 
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    
                    }})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            
            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report,)
            return status
        except Exception as e:
            raise SensorException(e,sys)
    """
    Purpose: 
    1. Detect data drift between two DataFrames.
    2. Compares the distributions of each column in the training (base) and testing (current) datasets using the Kolmogorov-Smirnov test.
    3. Updates a report with the p-value and drift status for each column.
    4. If the p-value is below the threshold, it indicates significant drift, and the status is set to False.
    5. Creates a directory for the drift report if it doesn't exist and writes the report to a YAML file.
    6. Returns True if no drift is detected; otherwise, returns False.
    7. Raises an exception if an error occurs.
    """
   

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            error_message = ""
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            #Reading data from train and test file location
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            #Validate number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message=f"{error_message}Train dataframe does not contain all columns.\n"
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message=f"{error_message}Test dataframe does not contain all columns.\n"
        

            #Validate numerical columns

            status = self.is_numerical_column_exist(dataframe=train_dataframe)
            if not status:
                error_message=f"{error_message}Train dataframe does not contain all numerical columns.\n"
            
            status = self.is_numerical_column_exist(dataframe=test_dataframe)
            if not status:
                error_message=f"{error_message}Test dataframe does not contain all numerical columns.\n"
            
            if len(error_message)>0:
                raise Exception(error_message)

            #Let check data drift
            status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact
        except Exception as e:
            raise SensorException(e,sys)
    """
    Purpose: 
    1. Orchestrate the data validation process.
    2. Initializes an empty error message string to collect any validation errors.
    3. Retrieves file paths for the training and testing datasets from the data ingestion artifact.
    4. Reads the datasets into DataFrames.
    5. Validates the number of columns and numerical columns for both DataFrames, accumulating error messages if any checks fail.
    6. Raises an exception if there are errors, ensuring that the process stops if the data is not valid.
    7. Calls the drift detection method to check for changes in the data distributions.
    8. Creates a DataValidationArtifact that summarizes the validation results, including the validation status and paths to the datasets and drift report.
    9. Logs the created artifact for tracking purposes.
    10. Returns the DataValidationArtifact, which can be used in subsequent steps of the machine learning pipeline.
    """

    