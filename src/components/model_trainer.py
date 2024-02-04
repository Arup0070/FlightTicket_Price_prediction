import sys,os
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
from sklearn.ensemble import RandomForestRegressor
from src.utils import Save_obj



@dataclass
class ModelTrainingConfig:
    trained_model_file_path= os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_traner_config=ModelTrainingConfig()

    def initiate_model_training(self,train_arr,test_arr):
        try:
            logging.info("spliting dependent and independent verials from train and test data")
            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            Ran_model=RandomForestRegressor(n_estimators= 300,
                                      min_samples_split =  8,
                                      min_samples_leaf = 3,
                                      max_features = 3,
                                      max_depth = 90,
                                      bootstrap = True)
            
            Ran_model.fit(x_train,y_train)


            Save_obj(
                 file_path=self.model_traner_config.trained_model_file_path,
                 obj=Ran_model
            )
            logging.info("Model trained and saved successfully")
        except Exception as e:
            logging.info("error occcerd during model trainning")
            raise CustomException(e,sys)