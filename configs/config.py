from src.entity.config_entity import *
from configs.path import *
from configs.settings import *

class ConfigurationManager:
    def get_data_ingestion_config(self):
        
        return(
            DataIngestionConfig(
            DATA_DIR=DATA_DIR_PATH,
            RAW_DATA_DIR=RAW_DIR_PATH,
            RAW_DATA_FILE=RAW_DATA_FILE_PATH,
            TRAIN_TEST_DIR=TRAIN_TEST_DIR_PATH,
            TRAIN_FILE=TRAIN_FILE_PATH,
            TEST_FILE=TEST_FILE_PATH,
        )
            )
        
    def get_data_validation_config(self):
        
        return(
            DataValidationConfig(
                REPORTS_DIR=REPOTRS_DIR_PATH,
                REPORTS_VALIDATION_FILE=REPORTS_VALIDATION_FILE_PATH
            )
        )
        
    def get_data_preproccessing_config(self):
        return (
            DataPreproccessing(
                PREPROCCESSED_DIR=PREPROCCESSED_DIR_PATH,
                PREPROCCESSED_TEST_FILE=PREPROCCESSED_TEST_FILE_PATH,
                PREPROCCESSED_TRAIN_FILE=PREPROCCESSED_TRAIN_FILE_PATH
            )
        )
    
    def get_data_transform_config(self):
        return(
            DataTransformConfig(
                    TRANSFORM_DATA_DIR=TRANSFORM_DATA_DIR_PATH,
                    TRANSFORM_TEST_FILE=TRANSFORM_TEST_FILE_PATH, 
                    TRANSFORM_TRAIN_FILE=TRANSFORM_TRAIN_FILE_PATH ,
                    PREPROCCESSOR_DIR=PREPROCCESSOR_DIR_PATH,
                    PREPROCCESSOR_FILE=PREPROCCESSOR_FILE_PATH
            )
        )