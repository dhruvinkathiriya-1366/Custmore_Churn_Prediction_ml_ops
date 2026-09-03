from src.entity.config_entity import *
from configs.path import *
from configs.settings import *

class ConfigurationManager:
    def get_data_ingestion_config(self):
        
        return(
            DataIngestionConfig(
            DATA_DIR=DATA_DIR_PATH,
            RAW_DATA_DIR=RAW_DIR_PATH,
            RAW_DATA_FILE=RAW_DATA_FILE_PATH 
        )
            )