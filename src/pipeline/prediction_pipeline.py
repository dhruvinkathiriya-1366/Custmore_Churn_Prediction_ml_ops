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
            prediction = model.predict(transformed_data)

            logger.info(f"Prediction completed: {prediction}")

            return prediction

        except Exception as e:
            raise MyException(e, sys)

    def predict_with_score(self, input_data: pd.DataFrame):
        try:
            import numpy as np
            logger.info("Starting detailed prediction pipeline with risk scoring")

            preprocessor = load_pkl(self.transform_config.PREPROCCESSOR_FILE)
            model = load_pkl(self.model_trainer_config.MODELS_FILE)

            transformed_data = preprocessor.transform(input_data)
            predictions = model.predict(transformed_data)

            probabilities = []
            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(transformed_data)[:, 1]
            elif hasattr(model, "decision_function"):
                decision_scores = model.decision_function(transformed_data)
                probabilities = 1.0 / (1.0 + np.exp(-decision_scores))
            else:
                probabilities = [1.0 if p == 1 else 0.0 for p in predictions]

            results = []
            for pred, prob in zip(predictions, probabilities):
                prob_float = float(prob)
                risk_level = "High" if prob_float >= 0.65 else ("Medium" if prob_float >= 0.40 else "Low")
                results.append({
                    "prediction": int(pred),
                    "label": "Churn" if int(pred) == 1 else "Retained / Stayed",
                    "churn_probability": round(prob_float * 100, 2),
                    "risk_level": risk_level
                })

            return results

        except Exception as e:
            raise MyException(e, sys)
