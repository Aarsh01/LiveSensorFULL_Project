from dotenv import load_dotenv
# Loads environment variables from a .env file, allowing for configuration without hardcoding values.

import pymongo

from sensor.constant.database import DATABASE_NAME
from sensor.constant.env_variable import MONGODB_URL_KEY
import certifi
# This line retrieves the path to the CA certificates provided by the certifi package, which is used for secure connections.

import os 
import logging 

load_dotenv()


# MongoDBClient: A class that manages the connection to a MongoDB database.
# client: A class variable that holds the MongoDB client instance. It's initialized to None.
class MongoDBClient:
    client = None

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        """
        Initializes the MongoDB client and connects to the specified database.

        Args:
            database_name (str): The name of the database to connect to. Defaults to DATABASE_NAME.
        
        Raises:
            ValueError: If the MongoDB URL is not found in the environment variables.
        """
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                
                if mongo_db_url is None:
                    logging.error("MongoDB URL not found in environment variables.")
                    raise ValueError("MongoDB URL not found in environment variables.")

                logging.info(f"Retrieved MongoDB URL: {mongo_db_url}")

                if "localhost" in mongo_db_url:
                    MongoDBClient.client = pymongo.MongoClient(mongo_db_url)
                else:
                    MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=certifi.where())  # TLS/SSL
                
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info(f"Connected to database: {self.database_name}")
        except Exception as e:
            logging.error(f"Error initializing MongoDB client: {e}")
            raise
