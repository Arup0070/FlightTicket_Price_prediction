from flask import Flask,request,render_template,jsonify
from src.pipeline.prediction_pipeline import CustomData,PredictPipeline
from datetime import datetime
import datetime as d
from pytz import timezone 

application=Flask(__name__)

app=application

@app.route('/')

def home_page():
    return render_template('index.html')

@app.route('/predict',methods = ['GET','POST'])

def predict_datapoint():
    if request.method=='GET':
        return render_template('form.html')

    else:
         source_city = request.form.get('source_city'),
         destination_city = request.form.get('destination_city'),
         departure_time = request.form.get('departure_time'),
         stops = request.form.get('stops'),
         arrival_time = request.form.get('arrival_time'),
         Class = request.form.get('Class'),
         Duration_in_min= int(request.form.get('Duration_in_min')),
         days_left = int(request.form.get('days_left'))
         airline_li=['SpiceJet', 'AirAsia', 'Vistara', 'GO_FIRST', 'Indigo', 'Air_India']
         price_dict={}
         if source_city == destination_city:
             return render_template('error.html')
         else:
                for i in airline_li:
                        data=CustomData(
                            airline= i,
                            source_city = source_city[0],
                            destination_city = destination_city[0],
                            departure_time = departure_time[0],
                            stops = stops[0],
                            arrival_time = arrival_time[0],
                            Class = Class[0],
                            Duration_in_min= Duration_in_min[0],
                            days_left = days_left
                            )
                        final_new_data=data.get_data_as_dataframe()
                        predict_pipeline=PredictPipeline()

                        pred=predict_pipeline.predict(final_new_data)
                        results=round(pred[0],2)
                        price_dict[i]=results

                return render_template('results.html',SpiceJet=f"₹ {price_dict['SpiceJet']}",
                                                          AirAsia=f"₹ {price_dict['AirAsia']}",
                                                          Vistara=f"₹ {price_dict['Vistara']}",
                                                          GO_FIRST=f"₹ {price_dict['GO_FIRST']}",
                                                          Indigo=f"₹ {price_dict['Indigo']}",
                                                          Air_India=f"₹ {price_dict['Air_India']}",
                                                          Placefrom=source_city[0],
                                                          Placeto=destination_city[0],
                                                          Date = f"Departure Date {(datetime.now(timezone('Asia/Kolkata'))+d.timedelta(days_left)).strftime('%d/%m/%Y')}"
                                            )

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)