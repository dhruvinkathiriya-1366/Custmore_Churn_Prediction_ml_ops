import sys
from configs.config import ConfigurationManager
from src.logger import logger
from src.exception import MyException
from src.utils.common import (read_csv,load_csv,dump_pkl)
from sklearn.svm import SVC
import pandas as pd

class ModelTrainer:
    def __init__(self):
        try:
            self.manager=ConfigurationManager()
            self.model_trainer_config=self.manager.get_model_trainer_config()
            self.transform_config=self.manager.get_data_transform_config()
        
        except Exception as e:
            raise MyException(e,sys)
    
    def split_x_y(self):
        
        try:
            logger.info("read the transformed data from the csv")
            x_train_path=self.transform_config.TRANSFORM_TRAIN_FILE
            x_test_path=self.transform_config.TRANSFORM_TEST_FILE
            y_train_path=self.transform_config.TRANSFORM_Y_TRAIN_FILE
            y_test_path=self.transform_config.TRANSFORM_Y_TEST_FILE
            
            x_train=read_csv(x_train_path)
            x_test=read_csv(x_test_path)
            y_train=read_csv(y_train_path).squeeze()
            y_test=read_csv(y_test_path).squeeze()
            
            logger.info("read x and y data successfully")
            
            return (x_train,y_train,x_test,y_test)
        
        except Exception as e:
            raise MyException(e,sys)
    
    def train_model(self):
        
        try:
            logger.info("initialize the model")
            model=SVC(
                    class_weight='balanced',
                    kernel='rbf',
                    C=1,
                    gamma=0.001
                    )
            return model
        except Exception as e:
            raise MyException(e,sys)
        
    def intiate_model_Trainer(self):
        try:
            logger.info("split the train and test as x and y")
            x_train,y_train,x_test,y_test=self.split_x_y()
            logger.info("train the model with passing x and y train_data")
            model=self.train_model()
            
            logger.info("start the model training.....")
            model.fit(x_train,y_train)
            logger.info("train model successfully")
            logger.info("save the model .pkl file")
            self.model_trainer_config.MODELS_DIR.mkdir(parents=True,exist_ok=True)
            dump_pkl(model,self.model_trainer_config.MODELS_FILE)
            
            logger.info("predict based on the test data")
            test_pred=model.predict(x_test)
            train_pred=model.predict(x_train)
            
            logger.info("save the prediction as csv")
            test_pred_df=pd.DataFrame(
                {
                    "Prediction":test_pred
                }
            )
            train_pred_df=pd.DataFrame(
                {
                    "Prediction":train_pred    
                }
            )
            load_csv(self.model_trainer_config.PREDICTION_TEST_FILE,test_pred_df)
            load_csv(self.model_trainer_config.PREDICTION_TRAIN_FILE,train_pred_df)
            logger.info("complete the training session of the model")
        except Exception as e:
            raise MyException(e,sys)
         
if __name__ =="__main__":
    model_trainer=ModelTrainer()
    model_trainer.intiate_model_Trainer()
            
            
        