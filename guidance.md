# In requirement.txt :
    # # -r why? beacuse it will read the file .txt one by one and install them.... 
    # pandas
    # numpy 
    # scikit-learn
    # python-dotenv
    # -e .
    # # to make the code readibility and if anyone else want to use the code he/she can.. # editable mode
    # # why? generally setup.py file is run then req.txt is run , So no to do again and again for running the setup.py file we add -e . at the last in req.txt, which triggers the setup.py file at the end and run the find_package() method.

    """
    pymongo[srv]==4.2.0
    pandas
    numpy
    scikit-learn
    pymongo
    # python-dotenv

    # -e .   #editable mode 
*********************************************************************************************************
# In main.py & sensor.exception:
    
    from sensor.exception import SensorException
    import sys

    def test_exception():
        try:
            a=1/0
        except Exception as e:
            raise SensorException(e,sys)

    if __name__=='__main__':
        try:
            test_exception()
        except Exception as e:
            print(e)

Output: 
PS D:\Bakchodi\LiveSensor> & C:/Users/aarsh/AppData/Local/Programs/Python/Python312/python.exe d:/Bakchodi/LiveSensor/LiveSensor_FULL_MLProject/main.py
for reading the .env file
Error occured and the file name is [d:\Bakchodi\LiveSensor\LiveSensor_FULL_MLProject\main.py] and the lineNumber is [6] and error is [division by zero]

********************************************************************************************************************************************

# In main.py & logger.py

    from sensor.exception import SensorException
    import sys
    from sensor.logger import logging

    def test_exception():
        try:
            logging.info("Error present!") # No uppercase of info
            a=1/0
        except Exception as e:
            raise SensorException(e,sys)

    if __name__=='__main__':
        try:
            test_exception()
        except Exception as e:
            print(e)

Output: 
logs folder is build.
In terminal:
PS D:\Bakchodi\LiveSensor> & C:/Users/aarsh/AppData/Local/Programs/Python/Python312/python.exe d:/Bakchodi/LiveSensor/LiveSensor_FULL_MLProject/main.
py
for reading the .env file
Error occured and the file name is [d:\Bakchodi\LiveSensor\LiveSensor_FULL_MLProject\main.py] and the lineNumber is [8] and error is [division by zero]


********************************************************************************************************************************************

# why .env file:
1. Security: Protects sensitive data (like passwords and API keys) from being exposed in version control.
2. Configuration: Centralizes and simplifies managing environment-specific settings.
3. Portability: Facilitates easy replication and sharing of configurations across different systems.
4. Flexibility: Allows dynamic configuration changes without altering the code.
5. Ease of Use: Provides straightforward integration with code via libraries like python-dotenv .

********************************************************************************************************************************************
# How we can load our dataset into mongoDB server :

### MongoDB pe kya karna hai:
1. make project in mongoDB
2. make cluster0 
3. give permissions to the yourself by making yourself user 

### Coming to vs code file:
1. make .env file paste the mongoDB connection url with the name of "MONGO_DB_URL"
2. to have the access of the file install "load_dotenv" library and write code in __init__.py file in sensor folder 
3. Build 2 python file in sensor i.e "config.py" and "utils.py"
4. a. In config file:/n
      - a.1. The code is designed to encapsulate the retrieval of a MongoDB connection URL from an environment variable,
      - a.2. Establish a connection to a MongoDB database using that URL.
   b. In utils file:
      b.1 It define a function, which help us to load the dataset into the mongoDB cluster. 
5. After that import them in main.py 
6. Provide the database name, collection name, dataset location path and just run
7. After running the main.py file dataset it loaded into the mongoDB cluster server

********************************************************************************************************************************************

# Sensor Fault Detection High Level Code Flow
## Start:
1. Build all folders in sensor folder i.e (cload_storage, components, configuration, constant, data_access, entity, pipeline).
2. Make them package by building "__init__.py" file i each folder. 
- Decide the variables in "sensor.constant.training_pipeline.__init__.py" 
- Do the coding stuff in 2 files in sensor.entity folder i.e "config_entity.py" and then "artifact_entity.py".

### Step - 1: Data Ingestion

    - In config_entity.py file: class name "DataIngestionConfig"
        a. set the path from artifacts to train.csv, test.csv, sensor.csv datasets. It is well explained there. 

    - In artifact_entity.py: class name "DataIngestionArtifact"
        a. Straightforward way to encapsulate the paths of training and testing datasets in a structured manner.

    - **To build the file "sensor.component.data_ingestion.py", we have 2 files ready:
        1. files in sensor.entity folder,
        2. mongoDb connection to have the dataset from mongoDB server that we have loaded with the help of two files: 
            2.1. sensor.config.py
            2.2. sensor.utils.py
            # Files in sensor.entity folder - Done

            # MongoDb connection:
                a. assign the keys in sensor.constant.env_variables.py (like - MONGODB_URL_KEY, AWS_ACCESS_KEY_ID_ENV_KEY, AWS_SECRET_ACCESS_KEY_ENV_KEY, REGION_NAME)
                
                b. assign the name of (DATABASE_NAME, COLLECTION_NAME) in sensor.constant.database.py. It should be same as that of the name when loading data in mongoDB cluster0. 
                
                c. Now coming to sensor.configuration.mongodb_db_connection :
                    1. Loads the MongoDB URL from environment variables.
                    2. Connects to the database, handling both local and secure connections.
                    3. Provides access to the specified database while logging any errors that may occur during the initialization process.
                
                d. Now coming to sensor.data_access.sensor_data :
                    1. The SensorData class serves as a bridge between a MongoDB database and Pandas DataFrames, enabling:
                        1.1. Data Import: Users can easily import data from CSV files into MongoDB, which is useful for data ingestion processes.
                        1.2. Data Export: Users can export entire collections from MongoDB into DataFrames, facilitating data analysis and manipulation using Pandas.
            
        3. Now coming to sensor.component.data_ingestion.py :
            1. Integrate Data Sources: Facilitate the extraction of data from a MongoDB database and prepare it for machine learning workflows.
            2. Data Management: Handle the ingestion of data, including exporting it to a feature store and splitting it into training and testing sets.
            3. Artifact Management: Create artifacts that can be used later in the machine learning pipeline for model training and evaluation.
            
        4. Now coming to sensor.pipeline.training_pipeline.py :
            1. Manage the Training Pipeline: It orchestrates the various components of the training pipeline, starting with data ingestion.
            2. Streamline Data Preparation: By encapsulating the data ingestion process, it simplifies the workflow of preparing data for machine learning.
            3. Error Handling: It provides a structured way to handle exceptions that may arise during the pipeline execution.

        5. Now run the main.py file, then artifacts ki ek folder build hoga.
        
        * Use the mongoDB_URL_KEY of Prince Katriya Sir, mine not working. Why? NOT KNOWN!
            ***- In requirement.txt, write pymongo[srv]==<version> instead of pymongo.

********************************************************************************************************************************************
### Potential Uses of the YAML File:
    1. Data Preprocessing: The YAML file can be used as a configuration file for data preprocessing tasks, such as data cleaning transformation, and feature selection.
    2. Machine Learning: The YAML file can serve as a configuration file for machine learning tasks, specifying which columns to use as features, which column is the target variable, and which columns to drop.
    3. Data Analysis: The YAML file can be used to guide data analysis tasks, specifying which columns to focus on, which columns to exclude, and what data types to expect

********************************************************************************************************************************************


### Step - 2: Data Validation
    - Why?
        : Train and test dataset are read 
        : Validates the presence of required columns in both sets., with the help of .yaml file 
        : Detects the data drift between both the sets. - (if dataset follows time series then after some period of time there is difference between the train and test datasets.)
    
    - **To build the file "sensor.component.data_validation.py" :
        
        1. build the .yaml file in config folder.

        2. Make new folder "utils" in sensor to read the .yaml file.
        
        3. Declare the variables in "sensor.constant.training_pipeline" folder for input for Data Validation.
        
        4. Declare the variable in "sensor.entity.artifact_entity" file for output for Data Validation.

        5. Write code in sensor.component.data_validation.py, importing all.
            5.1. The DataValidation class is designed to ensure that the datasets used in a machine learning pipeline are valid, consistent, and suitable for modeling. 
            5.2. By performing checks on the structure and content of the data, as well as monitoring for changes over time, the class helps maintain the quality of the data, which is crucial for building reliable machine learning models. 
            5.3. This proactive approach to data validation minimizes the risk of errors and improves the robustness of the overall machine learning process.

        6. Write code for dataValidation in "pipeline.training_pipeline.py" file.
        
        7. Run main.py 
    
********************************************************************************************************************************************
### Saving the Transformed Data ( save_numpy_array_data ):
1. Transforming raw data can be a time-consuming process, especially if the dataset is large or the preprocessing steps are complex. 
2. By saving the transformed data as numpy arrays, we can avoid re-running the entire preprocessing pipeline every time the transformed data is needed. 
3. Instead, we can directly load the preprocessed data from the saved numpy arrays, which is much faster and more efficien

********************************************************************************************************************************************

### Step - 3: Data Transformation
    - Why?


    - **To build the file "sensor.component.data_transformation.py" :
        1. make folder in sensor name as "ml", make them package also.
        2. Wriite code in utils for "save numpy data in file", "load numpy data in file", "save object", which can be used multiple times in the project.
        3. Write code in ml.model.estimator.py file to convert categorical Target column in numerical one. 
        4. Write down the output of the data transformation -(transformed_object_file_path, transformed_train_file_path, transformed_test_file_path) .
        5. Build the path in config_entity for data-transformation file.
        6. All the stuff of preprocessing are done in data_transforamtion.py. 
        7. Write code for dataValidation in "pipeline.training_pipeline.py" file.
        8. run the pipeline in main.py
    

### Step - 4: Model Training 
    -Why?
        1. Config - load train.csv, test.csv files
        2. split
        3. Training
        4. Prediction
        5. Accuracy
        6. Overfitting/Underfitting
        7. Model save
        8. Artifact
    
    - **To build the file "sensor.component.model_trainer.py" :
    



### Step - 5: Model Evaluation 
    -Why?
    
    - **To build the file "sensor.component.model_evaluation.py" :

### Step - 6: Model Pusher 
    -Why?
    
    - **To build the file "sensor.component.model_pusher.py" :


