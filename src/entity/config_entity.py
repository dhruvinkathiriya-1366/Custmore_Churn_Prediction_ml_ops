from dataclasses import dataclass
from pathlib import Path 

@dataclass
class DataIngestionConfig:
    DATA_DIR:Path
    RAW_DATA_DIR:Path
    RAW_DATA_FILE:Path