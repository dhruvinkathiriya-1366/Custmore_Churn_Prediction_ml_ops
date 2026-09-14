import sys
import pandas as pd

from src.logger import logger
from src.exception import MyException
from configs.config import ConfigurationManager
from src.utils.common import load_pkl


class PredictionPipeline:

    def __init__(self):
        try:
            self.manager = ConfigurationManager()

            self.transform_config = self.manager.get_data_transform_config()
            self.model_trainer_config = self.manager.get_model_trainer_config()
            

        except Exception as e:
            raise MyException(e, sys)

    def predict(self, input_data: pd.DataFrame):

        try:
            logger.info("Starting prediction pipeline")

            # Load preprocessor
            preprocessor = load_pkl(
                self.transform_config.PREPROCCESSOR_FILE
            )

            # Load trained model
            model = load_pkl(
                self.model_trainer_config.MODELS_FILE
            )

            logger.info("Preprocessor and model loaded successfully")

            # Transform input data
            transformed_data = preprocessor.transform(input_data)

            logger.info("Input data transformed successfully")

            # Make prediction
            prediction=model.predict(transformed_data)

            logger.info(f"Prediction completed: {prediction}")

            return prediction

        except Exception as e:
            raise MyException(e, sys)
