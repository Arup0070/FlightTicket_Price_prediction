from src.exception import CustomException
from src.logger import logging
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OrdinalEncoder                                
from dataclasses import dataclass
import os,sys
import pandas as pd
from src.utils import Save_obj
import numpy as np

@dataclass
class Datatransformationconfig:
    preprocessor_file_obj_path = os.path.join('artifacts','preprocessor.pkl')

class Datatransformation:

    def __init__(self):
        self.data_transformation_config=Datatransformationconfig()
        
    def get_data_transformation_obj(self):
        try:
            logging.info("Data Transformation process Started")
            cata_col=['airline','source_city','departure_time','stops','arrival_time','destination_city','Class']
            num_col=[ 'days_left','Duration_in_min']
            num_pipeline=Pipeline(
                                steps=[
                                        ('imputer',SimpleImputer(strategy="median")),
                                        ('Scaler',StandardScaler())
                                      ]
                                    )
            cat_pipeline=Pipeline(
                                steps=[
                                        ('imputer',SimpleImputer(strategy="most_frequent")),
                                        ('encoder',OrdinalEncoder()),
                                        ('scaler',StandardScaler())
                                      ]
                                   )
            
            preprocessor=ColumnTransformer([
                                         ('Num_pipeline',num_pipeline,num_col),
                                         ('Cat_piptline',cat_pipeline,cata_col)
                                            ]
                                            )
            return preprocessor

        except Exception as e:
            logging.info("Error in data transformation module")
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            logging.info("Data Traformation started")
            train_data=pd.read_csv(train_path)
            test_data=pd.read_csv(test_path)
            logging.info("Train test Data read from file successfull")

            target_col="price"
            
            preprocessing_obj=self.get_data_transformation_obj()

            input_train_df=train_data.drop(target_col,axis=1)
            target_train_df=train_data[target_col]

            input_test_df=test_data.drop(target_col,axis=1)
            target_test_df=test_data[target_col]

            logging.info("Data separation done for input and target feature and preprocessing Started ")

            train_arr=preprocessing_obj.fit_transform(input_train_df)
            test_arr=preprocessing_obj.transform(input_test_df)

            train_arr = np.c_[train_arr,np.array(target_train_df)]
            test_arr = np.c_[test_arr,np.array(target_test_df)]

            Save_obj(
                file_path=self.data_transformation_config.preprocessor_file_obj_path,
                obj=preprocessing_obj
            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_file_obj_path
            
            )
        
            logging.info("Data transformation done successfully")

        except Exception as e:
            logging.info("error in data transformation module")
            raise CustomException(e,sys)







