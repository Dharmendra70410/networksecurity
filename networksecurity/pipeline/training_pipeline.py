#lec 296 training pipeline implementation 

import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer


from networksecurity.entity.config_entity import(
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
    #1
    def start_data_ingestion(self):
        try:
            self.dataingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Start data ingestion")
            #now initialize the DataIngesion class
            data_ingestion=DataIngestion(data_ingestion_config=self.dataingestion_config) 
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion() #now run Data_ingestion.py file
            logging.info(f"Data Ingestion completed and artifact:{data_ingestion_artifact}") #just in log file artifact store(to cross verify,not mandatory)
            return data_ingestion_artifact

        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    # 2nd component
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact):
        try:
            data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config) #path banana kaam hai
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)
            logging.info("initiate teh data Valadation")
            data_validation_artifact=data_validation.initiate_data_validation() #here data_validation file run, data validation started here, return data_validation_artificat
            logging.info("data valadatiion completed")
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    
    #3 component
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config) #path banao
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact, data_transformation_config=data_transformation_config)
                
            data_transformation_artifact = data_transformation.initiate_data_transformation() #data_transformationfile run her, and return transformation=artificat
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    #4 component
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            self.model_trainer_config: ModelTrainerConfig = ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config,
            )

            model_trainer_artifact = model_trainer.initiate_model_trainer() #returnmodel_trainer_aritficat, see model_trainer.py file 

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifict=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            return model_trainer_artifict
        except Exception as e:
            raise NetworkSecurityException(e, sys)
