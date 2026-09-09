import sys 
from src.logger import logger 
from src.exception import MyException 
from configs.config import ConfigurationManager 
from sklearn.compose import ColumnTransformer 
from configs.settings import NOT_SCALLNEED 
from src.utils.common import read_csv,load_csv,dump_pkl
from sklearn.pipeline import Pipeline 
from sklearn.impute import SimpleImputer 
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder,RobustScaler,StandardScaler 
from pandas import DataFrame 
import pandas as pd 

class DataTransform: 
    def __init__(self): 
        try: 
            self.manager=ConfigurationManager() 
            self.config=self.manager.get_data_transform_config() 
            
        except Exception as e: raise MyException(e,sys) 
        
    def fetch_column(self,df :DataFrame): 
        try: 
            cat_col=df.select_dtypes(include="object").columns 
            numeric_col=df.select_dtypes(include="number").columns 
            ordinal_col=['Contract'] 
            nominal_col=[col for col in cat_col if col not in ordinal_col] 
            self.not_scallneed=NOT_SCALLNEED 
            scaling_col=[col for col in numeric_col if col not in self.not_scallneed] 
            robust_col = []
            standard_col = [] 
            for col in scaling_col: 
                Q1 = df[col].quantile(0.25) 
                Q3 = df[col].quantile(0.75) 
                IQR = Q3 - Q1 
                lower = Q1 - 1.5 * IQR 
                upper = Q3 + 1.5 * IQR 
                outliers = df[ (df[col] < lower) | (df[col] > upper) ]
                if len(outliers) > 0: robust_col.append(col) 
                else: standard_col.append(col) 
            return (ordinal_col,nominal_col,robust_col,standard_col) 
        except Exception as e: raise MyException(e,sys) 
        
        
    def data_transform(self,ordinal_col,nominal_col,robust_col,standard_col): 
            try: 
                 logger.info("intiate the ordinal_pipeline") 
                 Ordinal_pipeline=Pipeline([ ('imputetion',SimpleImputer(strategy="most_frequent")), ('ordinaltransform',OrdinalEncoder()) ]) 
                 logger.info("intiate the onehot_pipeline") 
                 onehot_pipeline=Pipeline([ ('imputetion',SimpleImputer(strategy="most_frequent")), ('onehottransform',OneHotEncoder(handle_unknown="infrequent_if_exist",min_frequency=2)) ]) 
                 logger.info("intiate the Transformer") 
                 Transformer=ColumnTransformer( transformers=( 
                                                              ["ordinal",Ordinal_pipeline,ordinal_col], 
                                                              ["onehot",onehot_pipeline,nominal_col], 
                                                              ['Sscale',StandardScaler(),standard_col], 
                                                              ['Rscale',RobustScaler(),robust_col] ), 
                                                              remainder="passthrough" ) 
                 return Transformer 
            except Exception as e:
                raise MyException(e,sys)
            
             
    def intiate_data_transformation(self): 
            try: 
                self.ingestion_config=self.manager.get_data_ingestion_config() 
                self.train_path=self.ingestion_config.TRAIN_FILE 
                self.test_path=self.ingestion_config.TEST_FILE 
                self.train_df=read_csv(self.train_path) 
                self.test_df=read_csv(self.test_path) 
            
                logger.info("fetch the column for the transfom the data") 
            
                trainordinal_col,trainnominal_col,trainrobust_col,trainstandard_col=self.fetch_column(self.train_df) 
                testordinal_col,testnominal_col,testrobust_col,teststandard_col=self.fetch_column(self.test_df) 
            
                logger.info("fetch required column") 
                logger.info("start the data_transformation") 
            
                self.preproccessor=self.data_transform(trainordinal_col,trainnominal_col,trainrobust_col,trainstandard_col) 
                self.preproccessor.fit(self.train_df) 
                self.transform_train=self.preproccessor.transform(self.train_df) 
                self.transform_test=self.preproccessor.transform(self.test_df) 
            
                if hasattr(self.transform_train, "toarray"): self.transform_train = self.transform_train.toarray() 
                if hasattr(self.transform_test, "toarray"): self.transform_test = self.transform_test.toarray() 
                train_df = pd.DataFrame(self.transform_train) 
                test_df = pd.DataFrame(self.transform_test)
             
                logger.info("data transform successfully") 
                logger.info("load the train,test transformed data") 
                self.config.TRANSFORM_DATA_DIR.mkdir(parents=True,exist_ok=True) 
                load_csv(self.config.TRANSFORM_TRAIN_FILE,train_df) 
                load_csv(self.config.TRANSFORM_TEST_FILE,test_df) 
                self.config.PREPROCCESSOR_DIR.mkdir(parents=True,exist_ok=True)
                 
                dump_pkl(self.preproccessor,self.config.PREPROCCESSOR_FILE) 
                logger.info("successfi=ully load the .csv and .pkl file") 
            except Exception as e:
                raise MyException(e,sys) 
            
if __name__=="__main__": 
    data_transform=DataTransform() 
    data_transform.intiate_data_transformation()