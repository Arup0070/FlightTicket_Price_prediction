from src.logger import logging
from src.exception import CustomException
import os,sys
from src.utils import load_obj
import pandas as pd
import pickle

class PredictPipeline:
    def __init__(self) -> None:
        pass
    def predict(self,features):
        try:
            preprocessor_path=os.path.join("artifacts","preprocessor.pkl")
            model_path=os.path.join('artifacts','model.pkl')  

            preprocessor=load_obj(preprocessor_path)
            with open(model_path,'rb') as file_obj:
                    model= pickle.load(file_obj)
            #model=load_obj(model_path)

            data_sealed=preprocessor.transform(features)
            pred=model.predict(data_sealed)
            return pred         
            
        except Exception as e:
            logging.info("Error in model prediction process")
            raise CustomException(e,sys)

class CustomData:
    def __init__(self,airline: str ,
                      source_city: str,
                      departure_time: str,
                      stops : str,
                      arrival_time:str,
                      destination_city: str,
                      Class : str,
                      days_left: int,
                      Duration_in_min: int
                    ):
        self.airline=airline
        self.source_city=source_city
        self.departure_time=departure_time
        self.stops=stops
        self.arrival_time=arrival_time
        self.destination_city=destination_city
        self.Class=Class
        self.days_left=days_left
        self.Duration_in_min=Duration_in_min

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'airline':[self.airline],
                'source_city':[self.source_city],
                'departure_time':[self.departure_time],
                'stops':[self.stops],
                'arrival_time':[self.arrival_time],
                'destination_city':[self.destination_city],
                'Class':[self.Class],
                'days_left':[self.days_left],
                'Duration_in_min':[self.Duration_in_min]
            }
            df = pd.DataFrame(custom_data_input_dict)
            logging.info('Dataframe Gathered')
            return df
        except Exception as e:
            logging.info("Exception occerd in predection stage in dataframe module")
            raise CustomException(e,sys)
      



