import os
from configs.settings import (COLLECTION_NAME,DATABASE_NAME,)
from pymongo import MongoClient
from dotenv import load_dotenv
from src.logger import logger
from src.exception import MyException
import sys
import pandas as pd 

class MongoConfig:
    clien=None
    def __init__(self,db_name :str=DATABASE_NAME):
        
        try:
            load_dotenv()
            
            mongo_url=os.getenv("MONGODB_URL")
            MongoConfig.client=MongoClient(mongo_url)
            
            logger.info("connection established")
            self.clien=MongoConfig.client
            self.data_base=self.client[db_name]
            
        except Exception as e:
            raise MyException(e,sys)
        
    def export_data(self):
        
        try:
            
            logger.info("fetching data from the database")
        
            self.collection=self.data_base[COLLECTION_NAME]
            
            logger.info("fetch data from the database successfully")
            
            df=pd.DataFrame(self.collection.find({},{"_id":0}))
            logger.info("json is convert into the dataframe")
            return df
        
        except Exception as e:
            raise MyException(e,sys)