from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionArtifact:

    RAW_DATA_FILE: Path
    TRAIN_FILE: Path
    TEST_FILE: Path