import pandas as pd
import numpy as np
import json
from sensor.config import mongo_client
 
def dump_csv_file_to_mongodb_collection(file_path:str, database_name:str, collection_name:str) -> None:
    try:

        df= pd.read_csv(file_path)
        df.reset_index(drop=True,inplace=True)
        json_records=list(json.loads(df.T.to_json()).values())
        # 1. df.T - transform the df
        # 2. convert it into json file using .to_json()
        # 3. to convert it, load it using json.loads()
        # 4. we want only values so use .values()
        # 5. list them and save them in "json_records"
        

        mongo_client[database_name][collection_name].insert_many(json_records)
        
    except Exception as e :
        print(e)
