from configs.mongo_configuration import MongoConfig
from configs.config import ConfigurationManager
from src.logger import logger
from src.exception import MyException
import pathlib
import sys

class DataIngestion:
    
    def __init__(self):
        try:
          
          manager=ConfigurationManager()
          self.config=manager.get_data_ingestion_config()
        except Exception as e:
            raise MyException(e,sys)
         
    def initiate_data_ingestion(self):
        
        try:
            logger.info("start the data ingestion")
            
            mongo=MongoConfig()
            df=mongo.export_data()
            
            self.config.DATA_DIR.mkdir(parents=True,exist_ok=True)
            logger.info("successfully created data_dir")
            
            self.config.RAW_DATA_DIR.mkdir(parents=True,exist_ok=True)
            logger.info("successfully created raw_dir")
            
            df.to_csv(self.config.RAW_DATA_FILE,index=False)
            logger.info("successfully created raw.csv")
            
            logger.info("data is ingested")
            
            return self.config.RAW_DATA_FILE
        
        except Exception as e:
            raise MyException(e,sys)
    
if __name__=="__main__":
    
    dataingestion=DataIngestion()
    dataingestion.initiate_data_ingestion()