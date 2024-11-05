import sys
from typing import Optional
import numpy as np
import pandas as pd
import json
from sensor.configuration.mongodb_db_connection import MongoDBClient
from sensor.constant.database import DATABASE_NAME
from sensor.exception import SensorException
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SensorData:
    """
    This class helps to export entire MongoDB records as a pandas DataFrame.
    """

    def __init__(self):
   
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
            logger.info("MongoDB client initialized successfully.")

        except Exception as e:
            logger.error(f"Failed to initialize MongoDB client: {str(e)}")
            raise SensorException(e, sys)
        

    def save_csv_file(self, file_path: str, collection_name: str, database_name: Optional[str] = None) -> int:
        """
        Reads a CSV file and saves its contents to a MongoDB collection.

        :param file_path: Path to the CSV file.
        :param collection_name: Name of the collection to insert records into.
        :param database_name: Optional; name of the database.
        :return: Number of records inserted.
        """
        try:
            data_frame=pd.read_csv(file_path)
            data_frame.reset_index(drop=True, inplace=True)
            records = list(json.loads(data_frame.T.to_json()).values())

            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            result = collection.insert_many(records)
            logger.info(f"Inserted {len(result.inserted_ids)} records into {collection_name}.")
            return len(result.inserted_ids)
        
        except FileNotFoundError:
            logger.error(f"CSV file not found: {file_path}")
            raise SensorException(f"CSV file not found: {file_path}", sys)
        
        except pd.errors.EmptyDataError:
            logger.error("CSV file is empty.")
            raise SensorException("CSV file is empty.", sys)
        
        except Exception as e:
            logger.error(f"Error saving CSV file to MongoDB: {str(e)}")
            raise SensorException(e, sys)


    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Exports an entire MongoDB collection as a pandas DataFrame.

        :param collection_name: Name of the collection to export.
        :param database_name: Optional; name of the database.
        :return: DataFrame containing the collection data.
        """
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
                
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns:
                df = df.drop(columns=["_id"])

            df.replace({"na": np.nan}, inplace=True)
            logger.info(f"Exported {len(df)} records from {collection_name} as DataFrame.")
            return df
        
        except Exception as e:
            logger.error(f"Error exporting collection as DataFrame: {str(e)}")
            raise SensorException(e, sys)

