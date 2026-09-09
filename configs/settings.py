
ARTIFACTS_DIR_NAME="artifacts"
#mongo_db

DATABASE_NAME="proj1"
COLLECTION_NAME="proj1 data"

#data_ingestion

DATA_DIR_NAME="data"
RAW_DATA_DIR_NAME="raw"
RAW_DATA_DIR_FILE_NAME="raw.csv"
TRAIN_TEST_DIR_NAME="feature"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"
TEST_SPLIT_RATIO=0.2


#data_validation

REPOTRS_DIR_NAME="reports"
REPORTS_VALIDATION_FILE_NAME="validation.json"
SCHEMA_FILE_PATH="configs/schema.yaml"

#data_preprocessing

PREPROCCESSED_DIR_NAME="preproccessed"
PREPROCCESSED_TRAIN_FILE_NAME="train.csv"
PREPROCCESSED_TEST_FILE_NAME="test.csv"
  #clean_data:
DROP_COLUMN=['ZipCode','City','Quarter','State','Country','CustomerID','ChurnScore','ChurnCategory','ChurnReason','CLTV','CustomerStatus','Dependents','ReferredaFriend','InternetService']

#transform
TRANSFORM_DATA_DIR_NAME="transform"
TRANSFORM_TRAIN_FILE_NAME="train.csv"
TRANSFORM_TEST_FILE_NAME="test.csv"
PREPROCCESSOR_DIR_NAME="preproccessor"
PREPROCCESSOR_FILE_NAME="preproccessor.pkl"
NOT_SCALLNEED=['ZipCode','City','Quarter','State','Country','CustomerID','ChurnScore','ChurnCategory','ChurnReason','CLTV','CustomerStatus','Dependents','ReferredaFriend','InternetService']