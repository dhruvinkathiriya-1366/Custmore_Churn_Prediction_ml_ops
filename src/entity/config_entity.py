from dataclasses import dataclass
from pathlib import Path 

@dataclass
class DataIngestionConfig:
    DATA_DIR:Path
    RAW_DATA_DIR:Path
    RAW_DATA_FILE:Path
    TRAIN_TEST_DIR:Path
    TRAIN_FILE:Path
    TEST_FILE:Path
    
@dataclass
class DataValidationConfig:
    REPORTS_DIR:Path
    REPORTS_VALIDATION_FILE:Path

@dataclass
class DataPreproccessing:
  PREPROCCESSED_DIR :Path
  PREPROCCESSED_TEST_FILE :Path
  PREPROCCESSED_TRAIN_FILE :Path
  
@dataclass
class DataTransformConfig:
    TRANSFORM_DATA_DIR :Path
    TRANSFORM_TEST_FILE :Path
    TRANSFORM_TRAIN_FILE :Path
    PREPROCCESSOR_DIR :Path
    PREPROCCESSOR_FILE :Path