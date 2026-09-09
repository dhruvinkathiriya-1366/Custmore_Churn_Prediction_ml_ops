import yaml
import json
import sys
import joblib
from pathlib import Path
from src.exception import MyException
import pandas as pd
from pandas import DataFrame

def create_dir(path:Path):
    
    try:
        path.mkdir(
            parents=True,
            exist_ok=True
            )
    except Exception as e:
        raise MyException(e,sys)
    
def read_yaml(path:Path):
    
    try:
        
        with open(
            path,
            "r",
            encoding="utf-8"
            ) as file:
            content=yaml.safe_load(file)
            
            return content
    except Exception as e:
        raise MyException(e,sys)
    
def write_yaml(path:Path,data):
    
    try:
        
        with open(path,"w") as file:
            yaml.dump(data,file,sort_keys=False)
            
    except Exception as e:
            raise MyException(e,sys)
    
def read_json(path:Path):
    
    try:
        
        with open(path,"r",encoding="utf=8") as file:
            content=json.load(file)
            
            return content
        
    except Exception as e:
        raise MyException(e,sys)
    
def write_json(path:Path,data):
    
    try:
        
        with open(path,"w") as file:
            json.dump(data,file,sort_keys=False)
            
    except Exception as e:
        raise MyException(e,sys)
    
def read_csv(path:Path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        raise MyException(e,sys)        

def load_csv(path:Path,df:DataFrame):
    try:
         df.to_csv(path,index=False)
    
    except Exception as e:
        raise MyException(e,sys)

def dump_pkl(preproccessor,path):
    try:
        joblib.dump(preproccessor,path)
    except Exception as e:
        raise MyException(e,sys)