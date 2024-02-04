from src.logger import logging
from src.exception import CustomException
import pymongo
from pymongo import MongoClient
import pandas as pd
import sys
import os
import certifi
import pickle
from sklearn.ensemble import RandomForestRegressor

def MongoDBcoll():
    logging.info("Connecting to MongoDB database")
    try:
        ca= certifi.where()
        cluster = MongoClient("mongodb+srv://arup92327:Arup0070@cluster0.e9r83iz.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=ca)
        db=cluster["FlightDB"]
        coll=db["Flight_Data"]
        li=[]
        for i in coll.find({},{"_id":0,"flight":0}):
            li.append(i)
        Data=pd.DataFrame(li)
        logging.info(f"{Data.head()} \n Collected Data")
        cluster.close()
        return Data
    except Exception as e:
        logging.info("not able to collect data from MongoBD Data Base")
        raise CustomException(e,sys)

def Save_obj(file_path,obj):
    logging.info("file object Saveing process started")
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
        file_obj.close()
    except Exception as e:
        logging.info("Error in file obj save")
        raise CustomException(e,sys)
    
def load_obj(file_path):
    try:
        with open(file_path,'rb') as file_obj:
             return pickle.load(file_obj)
    except Exception as e:
        logging("error occured in Object load module")
        raise CustomException(e,sys)    

'''
if __name__=="__main__":
    ran=RandomForestRegressor()
    preprocessor_file_obj_path = os.path.join('artifacts','preprocessor.pkl')
    data = Save_obj(file_path=preprocessor_file_obj_path,obj=ran)
'''