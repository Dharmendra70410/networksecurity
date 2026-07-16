from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig

from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_validation import DataValidation
import sys


if __name__=='__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Initate the data ingestion ")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(dataingestionartifact)

    #lec 287
        data_validation_config=DataValidationConfig(trainingpipelineconfig) #path banana kaam hai
        data_validation=DataValidation(dataingestionartifact, data_validation_config)
        logging.info("initiate teh data Valadation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("data valadatiion completed")
        print(data_validation_artifact)
       

    except Exception as e:
           raise NetworkSecurityException(e,sys)