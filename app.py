from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/submit', methods=['POST'])
def submit():
    
    import numpy as np
    airline = int(request.form.get('airl'))
    airline_array=np.array([0,0,0,0,0,0,0,0,0])
    airline_array[airline-1]=1

    source = int(request.form.get('src'))
    source_array=np.array([0,0,0,0,0])
    source_array[source-1]=1
    
    destination = int(request.form.get('dest'))
    destination_array=np.array([0,0,0,0,0])
    destination_array[destination-1]=1

    from datetime import datetime, timedelta
    d_time = request.form.get('dep_time')
    a_time = request.form.get('arrival_time')
    current_date = datetime.now().date()
    dt1 = datetime.strptime(d_time, "%H:%M")
    dt2 = datetime.strptime(a_time, "%H:%M")
    dt1 = datetime.combine(current_date, dt1.time())
    dt2 = datetime.combine(current_date, dt2.time())
    if dt2 < dt1:
        dt2 += timedelta(days=1)
    duration = (dt2 - dt1).total_seconds() / 60

    total_stops = int(request.form.get('stops'))
    total_stops_array=np.array([0,0,0,0,0])
    total_stops_array[total_stops]=1

    additional_info = int(request.form.get('addinf'))
    additional_info_array=np.array([0,0,0,0,0,0,0,0,0])
    additional_info_array[additional_info-1]=1

    import pandas as pd
    date_of_journey = request.form.get('date')
    date_of_journey = pd.to_datetime(date_of_journey, format="%Y-%m-%d")
    month = date_of_journey.month
    day = date_of_journey.day
    week_of_year = date_of_journey.isocalendar().week

    if len(a_time) <= 5:
        next_day = 0
    else:
        next_day = 1

    arrival_time = pd.to_datetime(a_time, format='%H:%M').hour
    dep_time = pd.to_datetime(d_time, format='%H:%M').hour

    # input = np.concatenate(np.array([dep_time, arrival_time, duration, month, day, week_of_year, next_day]), 
    #                        airline_array, total_stops_array, additional_info_array, source_array, destination_array)

    dep_time = np.array([dep_time])
    arrival_time = np.array([arrival_time])
    duration = np.array([duration])
    month = np.array([month])
    day = np.array([day])
    week_of_year = np.array([week_of_year])
    next_day = np.array([next_day])

    input = np.concatenate((
        dep_time,
        arrival_time,
        duration,
        month,
        day,
        week_of_year,
        next_day,
        airline_array,
        total_stops_array,
        additional_info_array,
        source_array,
        destination_array
    ), axis=0)
    input = np.ndarray.tolist(input)
    input=[input]

    import requests

    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "dErnzVwz67vEC_oV02F_j7a_wVxYYIqUf0Ur8_3q_T7q"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
    API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": 
                       [{"fields": 
                         [
                             "Dep_Time", "Arrival_Time", "Duration", "Month", "Day", "WeekOfYear", "Next_Day",
                             "Airline_IndiGo","Airline_Air India","Airline_Jet Airways", "Airline_Jet Airways Business", "Airline_Air Asia",
                             "Airline_SpiceJet","Airline_GoAir","Airline_Vistara","Airline_Multiple carriers",
                             "Total_Stops_1 stop", "Total_Stops_2 stops","Total_Stops_3 stops", "Total_Stops_4 stops", "Total_Stops_non-stop",
                             "Additional_Info_No info", "Additional_Info_In-flight meal not included", "Additional_Info_No check-in baggage included",
                             "Additional_Info_1 Short layover","Additional_Info_1 Long layover", "Additional_Info_Change airports",
                             "Additional_Info_Business class","Additional_Info_Red-eye flight","Additional_Info_2 Long layover", 
                             "Source_Banglore","Source_Kolkata","Source_Delhi", "Source_Chennai", "Source_Mumbai", 
                             "Destination_Banglore", "Destination_Kolkata","Destination_Delhi","Destination_Cochin","Destination_Hyderabad"
                        ],
                        "values": input
                        }]
                        }
    print(payload_scoring)

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/5382e4f0-a894-4f50-8d0f-0830f352bd55/predictions?version=2021-05-01', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    if response_scoring.status_code == 200:
        response_scoring_data=response_scoring.json()
        output=response_scoring_data['predictions'][0]['values'][0][0]

    return render_template('submit.html', prediction_text=output)

if __name__ == '__main__':
    app.run()
