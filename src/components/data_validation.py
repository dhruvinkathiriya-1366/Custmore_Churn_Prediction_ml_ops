from src.entity.artifact_entity import DataValidationArtifact
from configs.config import ConfigurationManager
from src.logger import logger
from src.exception import MyException
from src.utils.common import *
from pandas import DataFrame
from configs.settings import SCHEMA_FILE_PATH
from configs.path import (TEST_FILE_PATH,TRAIN_FILE_PATH)


class DataValidation:
     
    def __init__(self):
        try:
            manager=ConfigurationManager()
            self.config=manager.get_data_validation_config()
            self.schema=read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e,sys)
        
    def validation_number_of_column(self,df:DataFrame):
        try:
            logger.info("validate the number of the column")
            status=len(df.columns)==len(self.schema['columns'])
            logger.info(f"validation of number of column is:[{status}]")
            
            return status
        except Exception as e:
            raise MyException(e,sys) from e
        
    def intiate_data_validation(self):
        try:
            logger.info("start the data validation")
            self.train_path=TRAIN_FILE_PATH
            self.test_path=TEST_FILE_PATH
            
            self.train_df=read_csv(self.train_path)
            self.train_status=self.validation_number_of_column(self.train_df)
            
            self.test_df=read_csv(self.test_path)
            self.test_status=self.validation_number_of_column(self.test_df)
            
            logger.info("data is validate the sucessfully")
            self.config.REPORTS_DIR.mkdir(parents=True,exist_ok=True)
            data={
                "no_of_column_train_status":self.train_status,
                "no_of_column_test_status":self.test_status
            }
            write_json(self.config.REPORTS_VALIDATION_FILE,data)
            
            logger.info("complate the validation")
            return DataValidationArtifact(
                TRAIN_STATUS=self.train_status,
                TEST_STATUS=self.test_status
            )
        except Exception as e:
            raise MyException(e,sys) from e
if __name__ == "__main__":
    data_validation = DataValidation()
    data_validation.intiate_data_validation()