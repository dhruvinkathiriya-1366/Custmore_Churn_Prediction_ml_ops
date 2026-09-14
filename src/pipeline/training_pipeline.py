import sys
from src.logger import logger
from src.exception import MyException
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_preproccess import Data_preproccessing
from src.components.data_transformation import DataTransform
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation


class TrainingPipeline:
    def __init__(self):
        pass

    def run_pipeline(self):
        try:
            logger.info("========== Starting Data Ingestion ==========")
            data_ingestion = DataIngestion()
            data_ingestion.initiate_data_ingestion()

            logger.info("========== Starting Data Validation ==========")
            data_validation = DataValidation()
            data_validation.initiate_data_validation()

            logger.info("========== Starting Data Preprocessing ==========")
            data_preprocessing = Data_preproccessing()
            data_preprocessing.intiate_data_preproccessing()

            logger.info("========== Starting Data Transformation ==========")
            data_transformation = DataTransform()
            data_transformation.intiate_data_transformation()

            logger.info("========== Starting Model Training ==========")
            model_trainer = ModelTrainer()
            model_trainer.intiate_model_Trainer()

            logger.info("========== Starting Model Evaluation ==========")
            model_evaluation = ModelEvaluation()
            model_evaluation.intialize_model_evaluation()

            logger.info("========== Training Pipeline Completed Successfully ==========")
            return {"status": "success", "message": "Training pipeline completed successfully"}

        except Exception as e:
            logger.error(f"Error in training pipeline: {e}")
            raise MyException(e, sys)


if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()
