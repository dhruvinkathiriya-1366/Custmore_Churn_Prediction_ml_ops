from configs.mongo_configuration import MongoConfig
from configs.config import ConfigurationManager
from configs.settings import TEST_SPLIT_RATIO
from src.logger import logger
from src.exception import MyException
from sklearn.model_selection import train_test_split
from src.entity.artifact_entity import DataIngestionArtifact
import pathlib
import sys

class DataIngestion:
    
    def __init__(self):
        try:
          manager=ConfigurationManager()
          self.config=manager.get_data_ingestion_config()
        except Exception as e:
            raise MyException(e,sys)
    
    def fetch_data(self):
        try:
                    logger.info("start the data ingestion")
                    
                    mongo=MongoConfig()
                    df=mongo.export_data()
                    
                    logger.info("succesfully data is fetched")
                    
                    return df
        except Exception as e:
            raise MyException(e,sys)
    
    def split_data(self,df):
        try:
            self.train_df,self.test_df=train_test_split(df,test_size=TEST_SPLIT_RATIO,random_state=42)
            logger.info("succesfully spli the data in to trai and test")
            return self.train_df,self.test_df
        except Exception as e:
            raise MyException(e,sys)
         
    def initiate_data_ingestion(self):
        
        try:
            logger.info("start the data ingestion")
            df=self.fetch_data()
            train_df,test_df=self.split_data(df)
                       
            self.config.DATA_DIR.mkdir(parents=True,exist_ok=True)
            logger.info("successfully created data_dir")
            
            self.config.RAW_DATA_DIR.mkdir(parents=True,exist_ok=True)
            logger.info("successfully created raw_dir")
            
            df.to_csv(self.config.RAW_DATA_FILE,index=False)
            logger.info("successfully created raw.csv")
            
            self.config.TRAIN_TEST_DIR.mkdir(parents=True,exist_ok=True)
            train_df.to_csv(self.config.TRAIN_FILE,index=False)  
            test_df.to_csv(self.config.TEST_FILE,index=False)       
            logger.info("data is ingested")
            
            return DataIngestionArtifact(
                   RAW_DATA_FILE=self.config.RAW_DATA_FILE,
                   TRAIN_FILE=self.config.TRAIN_FILE,
                   TEST_FILE=self.config.TEST_FILE
                   )

        except Exception as e:
            raise MyException(e,sys)
    
if __name__=="__main__":
    
    dataingestion=DataIngestion()
    dataingestion.initiate_data_ingestion()