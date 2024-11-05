from dataclasses import dataclass
# dataclass: This is a decorator from the dataclasses module that allows you to create classes that are primarily used to store data with less boilerplate code.

import os 
import pymongo


# to store data
@dataclass
class EnvironmentVariable:
    mongodb_db_url:str = os.getenv("MONGO_DB_URL") # This retrieves the value of the environment variable "MONGO_DB_URL"
    # MONGO_DB_URL is from .env file where we store the url of the mongoDB cluster0 for connection


env_var=EnvironmentVariable() # Make the object of the class
mongo_client=pymongo.MongoClient(env_var.mongodb_db_url)





    