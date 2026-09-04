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