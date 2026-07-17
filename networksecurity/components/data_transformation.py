import sys
import os
import numpy as np
import pandas as pd

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import  save_numpy_array_data,save_object

#lec 290

class DataTransformation:
    def __init__(self, data_valadation_artifact:DataValidationArtifact, data_transformation_config
                 :DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_valadation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    @staticmethod #read the train and test data #benefit of statis mehtod, don't need to initalize the object, you can directly call by class name
    def read_data(file_path)->pd.DataFrame:  #inside validatiion artiicate, i have my test train invalid test train file path
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def get_data_transformer_object(cls)->Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        """
        logging.info(
            "Entered get_data_transformer_pbject method of Transformation class"
        )
        try:
          imputer:KNNImputer =KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS) #HERE Data Tranformationinputer params consider as key value pair, ** help in it
          logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
          processor:Pipeline=Pipeline([("imputer",imputer)]) #pipeline object is created
          return processor
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
       


        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Entered initate_data_transformatin method of DataTranformation class")
        try:
            logging.info("Starting data transformation ")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            # #remove target varible #  after getting train dataframe and test dataframe, we have to do  knn )
            
            ##create independent and dependent feature
            #training datafrae
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN] #if we see , the result is -1 and 1 so, -1 replace with 0
            target_feature_train_df= target_feature_train_df.replace(-1, 0)

            
            #testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            #pipelining started
            preprocessor=self.get_data_transformer_object() #initilze the preprocessor
            
            preprocessor_object=preprocessor.fit(input_feature_train_df) #fit is only for input
            transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature=preprocessor_object.transform(input_feature_test_df) #transformed only for test (data likage)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df) ] #Column-wise concatenate (join columns).
            test_arr = np.c_[ transformed_input_test_feature, np.array(target_feature_test_df) ]

            #save numpy array data
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr, ) #accessed  by help config_entity
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object( self.data_transformation_config.transformed_object_file_path, preprocessor_object,)#This contains the Pipeline object, not data.

            save_object( "final_model/preprocessor.pkl", preprocessor_object,)
             #preparing artifacts

            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact #this is transfromation articat, used in next componet 



        except Exception as e:
            raise NetworkSecurityException(e, sys)