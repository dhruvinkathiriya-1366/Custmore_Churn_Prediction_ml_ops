import logging 
from pathlib import Path 
from datetime import datetime
 
ROOT_DIR=Path(__file__).resolve().parents[2]
LOG_DIR=ROOT_DIR/"logs"
LOG_DIR.mkdir(parents=True,exist_ok=True)

LOG_FILE=LOG_DIR/f"{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.log"

logging.basicConfig( filename=LOG_FILE, 
                    level=logging.INFO, 
                    format="[%(asctime)s] %(levelname)s - %(message)s",
                    datefmt="%d-%m-%Y %H:%M:%S"
                    )
logger=logging.getLogger(__name__)