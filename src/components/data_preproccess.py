import sys
from configs.config import ConfigurationManager
from src.logger import logger
from src.exception import MyException
from configs.settings import DROP_COLUMN
from src.utils.common import (read_csv,load_csv)
from pandas import DataFrame


class Data_preproccessing:
    
    def __init__(self):
      try:
            self.manager=ConfigurationManager()
            self.config=self.manager.get_data_preproccessing_config()
      except Exception as e:
          raise MyException(e,sys)
    
    def clean_data(self,df:DataFrame)->DataFrame:
      try:
          logger.info("drop the columns")
          self.drop_column=DROP_COLUMN
          self.drop_column_df=df.drop(columns=self.drop_column)
          logger.info("drop the duplicates")
          self.clean_df=self.drop_column_df.drop_duplicates()
          return self.clean_df
      except Exception as e:
          raise MyException(e,sys)
      
    def intiate_data_preproccessing(self):
        try: 
            logger.info("read csv for the preprocceing")
            
            
            self.ingestion_config=self.manager.get_data_ingestion_config()
            self.train_path=self.ingestion_config.TRAIN_FILE
            self.test_path=self.ingestion_config.TEST_FILE
            
            self.train_df=read_csv(self.train_path)
            self.test_df=read_csv(self.test_path)
            
            logger.info("start the data preproccessing")
            self.clean_train_df=self.clean_data(self.train_df)       
            self.clean_test_df=self.clean_data(self.test_df)
            
            logger.info("complate the preproccessing")
            logger.info("save the preprocess train_df and test_df")
            self.config.PREPROCCESSED_DIR.mkdir(parents=True,exist_ok=True)
            load_csv(self.config.PREPROCCESSED_TEST_FILE,self.test_df)
            load_csv(self.config.PREPROCCESSED_TRAIN_FILE,self.test_df)
            logger.info("compalate the preproccessing")
        except Exception as e:
            raise MyException(e,sys)
        
if __name__=='__main__':
    datapreproccess=Data_preproccessing()
    datapreproccess.intiate_data_preproccessing()