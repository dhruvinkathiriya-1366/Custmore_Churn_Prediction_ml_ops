import sys
from configs.config import ConfigurationManager
from src.logger import logger
from src.exception import MyException
from src.utils.common import (read_csv,load_csv,dump_pkl,load_pkl,read_yaml)
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
import pandas as pd

class ModelTrainer:
    def __init__(self):
        try:
            self.manager=ConfigurationManager()
            self.config=self.manager.get_model_trainer_config()
            self.ingestion_config=self.manager.get_data_ingestion_config()
            self.model_trainer_config=self.manager.get_model_trainer_config()
            self.transform_config=self.manager.get_data_transform_config()
        
        except Exception as e:
            raise MyException(e,sys)
    
    def split_x_y(self):
        
        try:
            logger.info("read the transform data from the csv")
            train_path=self.ingestion_config.TRAIN_FILE
            test_path=self.ingestion_config.TEST_FILE
            train_df=read_csv(train_path)
            test_df=read_csv(test_path)
            
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
    
    def train_model(self):
        
        try:
            logger.info("read params from the params.yaml")
            self.params=read_yaml(self.model_trainer_config.PARAMS_YAML_FILE)
            logger.info("intialize the model")
            model=SVC(
                    class_weight=self.params["MODEL"]["class_weight"],
                    kernel=self.params["MODEL"]["kernel"],
                    C=self.params["MODEL"]["c"],
                    gamma=self.params["MODEL"]["gamma"]
                    )
            return model
        except Exception as e:
            raise MyException(e,sys)
        
    def intiate_model_Trainer(self):
        try:
            logger.info("split the train and test as x and y")
            x_train,y_train,x_test,y_test=self.split_x_y()
            logger.info("train the model with passing x and y train_data")
            logger.info("load the processor.pkl file for transform new data")
            preproccessor=load_pkl(self.transform_config.PREPROCCESSOR_FILE)
            model=self.train_model()
            
            logger.info("sttart the model training.....")
            model_pipeline=Pipeline([
                ('transform',preproccessor),
                ('model',model)
            ])
            model_pipeline.fit(x_train,y_train)
            logger.info("trai model successfully")
            logger.info("save the model .pkl file")
            self.model_trainer_config.MODELS_DIR.mkdir(parents=True,exist_ok=True)
            dump_pkl(model_pipeline,self.model_trainer_config.MODELS_FILE)
            
            logger.info("predict based on the test data")
            test_pred=model_pipeline.predict(x_test)
            train_pred=model_pipeline.predict(x_train)
            
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
            logger.info("complate the traning sestion of the model")
        except Exception as e:
            raise MyException(e,sys)
         
if __name__ =="__main__":
    model_trainer=ModelTrainer()
    model_trainer.intiate_model_Trainer()
            
            
        