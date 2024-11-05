from dataclasses import dataclass

# # ***************** 1 **********************
# Output of Data-Ingestion 
@dataclass
class DataIngestionArtifact:
    """
    Class to represent the artifacts generated during data ingestion.

    Attributes:
        trained_file_path (str): Path to the training file.
        test_file_path (str): Path to the testing file.
    """
    trained_file_path: str
    test_file_path: str

@dataclass # Decorator # if you want to store data then use this decorator. 
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str

"""
The DataIngestionArtifact class is a straightforward way to encapsulate the paths of training and testing datasets in a structured manner, 
making it easier to manage data artifacts in a machine learning workflow. 
Using data classes enhances code readability and reduces boilerplate code, allowing developers to focus on functionality.
<<<<<<< HEAD
"""

# # ***************** 2 **********************
# Output of Data-Validation
@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str


# # ***************** 3 **********************
# Output of Data-Transformation
@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str


# # ***************** 4.1 **********************
# Output of Model-Trainer
@dataclass
class ClassificationMetricArtifact:
    f1_score: float
    precision_score: float
    recall_score: float


# # ***************** 4.2 **********************
# Output of Model-Trainer
@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact


# # ***************** 5 **********************
# Output of Model-Evaluation
@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    improved_accuracy: float
    best_model_path: str
    trained_model_path: str
    train_model_metric_artifact: ClassificationMetricArtifact
    best_model_metric_artifact: ClassificationMetricArtifact
    

# ***************** 6 **********************
# Output of Model-Pusher
@dataclass
class ModelPusherArtifact:
    saved_model_path:str   
    model_file_path:str
