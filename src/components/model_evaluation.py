import sys
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,confusion_matrix)
from configs.config import ConfigurationManager
from src.utils.common import (read_csv,write_json) 
from src.logger import logger
from src.exception import MyException

class ModelEvaluation: 
   def __init__(self):
       manager=ConfigurationManager()
       self.transform_config=manager.get_data_transform_config()
       self.model_trainer_config=manager.get_model_trainer_config()
       self.evaluation_config=manager.get_model_evauation_config()
   def evaluat_metrics(self,y_test,y_pred):
       try:
           logger.info("pass the y_test and y_pred in sid ethe merics")
           
           metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'confusion_metrics':confusion_matrix(y_test,y_pred)
          }
           return metrics
       except Exception as e:
           raise MyException(e,sys)
       
   def intialize_model_evaluation(self):
       try:
            y_test=read_csv(self.transform_config.TRANSFORM_Y_TEST_FILE).squeeze()
            y_pred=read_csv(self.model_trainer_config.PREDICTION_TEST_FILE).squeeze()
            
            logger.info("start the model evaluation")
            
            metrics=self.evaluat_metrics(y_test,y_pred)
            logger.info(f"accuracy:{metrics['accuracy']}")
            logger.info(f"precision:{metrics['precision']}")
            logger.info(f"recall:{metrics['recall']}")
            logger.info(f"F1_score:{metrics['f1_score']}")
            logger.info(f"confusion_metrics:{metrics['confusion_metrics']}")
            
            logger.info("write in json......")
            data=({
                'accuracy':metrics['accuracy'],
                'precision':metrics['precision'],
                'recall':metrics['recall'],
                'F1_score':metrics['f1_score'],
            })
            write_json(self.evaluation_config.METRICS_FILE,data)
            logger.info("complete the model evaluation")
       except Exception as e:
           raise MyException(e,sys)

if __name__=="__main__":
    model_evaluate=ModelEvaluation()
    model_evaluate.intialize_model_evaluation()