from configs.mongo_configuration import MongoConfig
from configs.config import ConfigurationManager
from configs.settings import TEST_SPLIT_RATIO
from src.logger import logger
from src.exception import MyException
from sklearn.model_selection import train_test_split
from src.entity.artifact_entity import DataIngestionArtifact
from src.utils.common import read_csv
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
        
    def split_x_y(self,train_df,test_df):
                
                try:
                    x_train=train_df.drop(columns=['ChurnLabel'])
                    y_train=train_df['ChurnLabel'].map({
                        'Yes':1,
                        'No':0
                        })
                    x_test=test_df.drop(columns=['ChurnLabel'])
                    y_test=test_df['ChurnLabel'].map({
                                    'Yes':1,
                                    'No':0
                                    })
                    logger.info("spit in to x and y successfully")
                    
                    return (x_train,y_train,x_test,y_test)
                except Exception as e:
                            raise MyException(e,sys)
         
    def initiate_data_ingestion(self):
        
        try:
            logger.info("start the data ingestion")
            df=self.fetch_data()
            train_df,test_df=self.split_data(df)
            x_train,y_train,x_test,y_test=self.split_x_y(train_df,test_df)
            self.config.DATA_DIR.mkdir(parents=True,exist_ok=True)
            logger.info("successfully created data_dir")
            
            self.config.RAW_DATA_DIR.mkdir(parents=True,exist_ok=True)
            logger.info("successfully created raw_dir")
            
            df.to_csv(self.config.RAW_DATA_FILE,index=False)
            logger.info("successfully created raw.csv")
            
            self.config.TRAIN_TEST_DIR.mkdir(parents=True,exist_ok=True)
            train_df.to_csv(self.config.TRAIN_FILE,index=False)  
            test_df.to_csv(self.config.TEST_FILE,index=False)
            y_test.to_csv(self.config.Y_TEST_FILE,index=False) 
            y_train.to_csv(self.config.Y_TRAIN_FILE,index=False)   
             
            logger.info("data is ingested")
            
            data_ingestion_artifacts=DataIngestionArtifact(
                   RAW_DATA_FILE=self.config.RAW_DATA_FILE,
                   TRAIN_FILE=self.config.TRAIN_FILE,
                   TEST_FILE=self.config.TEST_FILE
                   )
            return data_ingestion_artifacts

        except Exception as e:
            raise MyException(e,sys)
    
if __name__=="__main__":
    
    dataingestion=DataIngestion()
    dataingestion.initiate_data_ingestion()