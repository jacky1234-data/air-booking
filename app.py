import os
from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np
#Initialize the flask App
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
path = "D:\\Original-comp-edisk\\class material\\Professional Development\\Air Booking Completion Prediction"

yes_no = ["Yes","No"]

def convert(hour):
    if hour == 0:
        return "12:00 am"
    elif hour>=1 and hour <= 11:
        return str(hour) + ":00 am"
    elif hour == 12:
        return "12:00 pm"
    else:
        return str(hour - 12) + ":00 pm"
    
def convert_back(hour):
    if hour == "12:00 am":
        return 0
    if hour == "12:00 pm":
        return 12
    col = hour.find(":")
    ending = hour[-2:]
    return int(hour[:col]) if ending == "am" else int(hour[:col]) + 12

def standardize(value, mean, std):
    return (value - mean) / std

def yes_or_no(text):
    return 1 if text == "Yes" else 0

#default page of our web-app
@app.route('/')
def home():
    passenger_options = [i for i in range(1,6)]
    hours_converted = [convert(i) for i in range(24)]
    return render_template('index.html', passenger_opt = passenger_options, hour_opt = hours_converted,
                           want_bag_opt = yes_no, want_seat_opt = yes_no, want_meal_opt = yes_no)

#To use the predict button in our web-app
@app.route('/predict',methods=['POST'])
def predict():
    mean_table = {'num_passengers': 1.5912563497460102,
                'purchase_lead': 84.94058237670494,
                'length_of_stay': 23.044778208871644,
                'flight_hour': 9.066277348906043,
                'flight_duration': 7.27752429902804,
                'wants_extra_baggage': 0.6687732490700372,
                'wants_preferred_seat': 0.296968121275149,
                'wants_in_flight_meals': 0.42714291428342865}
    std_table = {'num_passengers': 1.0201672072261316,
                'purchase_lead': 90.45054838623565,
                'length_of_stay': 33.88717055207245,
                'flight_hour': 5.412568818896451,
                'flight_duration': 1.4968536458995547,
                'wants_extra_baggage': 0.4706591342166288,
                'wants_preferred_seat': 0.456926943503086,
                'wants_in_flight_meals': 0.4946683119019396}
    
    with open(path + "\\templates\\" + 'index.html', 'r') as file:
        html_content = file.read()

    passenger_select = request.form.get('num_passengers')
    purchase_lead = request.form.get('purchase_lead_val')
    length_of_stay = request.form.get('length_of_stay_val')
    flight_start = request.form.get('flight_hour')
    flight_duration = request.form.get('flight_duration_val')
    want_bag = request.form.get('wants_extra_baggage')
    want_seat = request.form.get('wants_preferred_seat')
    want_meal = request.form.get('wants_in_flight_meals')

    passenger_options = [i for i in range(1,6)]
    hours_converted = [convert(i) for i in range(24)]
    bag_options = yes_no
    seat_options = yes_no
    meal_options = yes_no

    standard_data = {}
    values = [passenger_select, purchase_lead, length_of_stay, flight_start, 
            flight_duration, want_bag, want_seat, want_meal]
    column_name = ['num_passengers', 'purchase_lead', 'length_of_stay', 'flight_hour', 
                   'flight_duration','wants_extra_baggage', 'wants_preferred_seat', 'wants_in_flight_meals']
    for i,j in zip(values, column_name):
        try:
            val = float(i)
            val = standardize(val, mean_table[j], std_table[j])
            standard_data[j] = [val]
        except:
            if ":" in i:
                val = convert_back(i)
            else:
                val = yes_or_no(i)  
            val = standardize(val, mean_table[j], std_table[j])
            standard_data[j] = [val]  
    
    complete = model.predict(pd.DataFrame(standard_data))[0]
    state = " not " if complete == 0 else " "

    result = "Flight booking is" + state + "completed"

    return render_template('index.html', pred = result,
                          purchase_lead_val=purchase_lead, passenger_opt = passenger_options, passenger=int(passenger_select),
                          length_of_stay_val = length_of_stay, hour_start = flight_start,hour_opt = hours_converted,
                           flight_duration_val = flight_duration, want_bag_val = want_bag, want_bag_opt = yes_no,
                           want_seat_val = want_seat, want_seat_opt = yes_no, want_meal_val = want_meal, want_meal_opt = yes_no)

@app.route('/clear',methods=['POST'])
def clear():
    passenger_options = [i for i in range(1,6)]
    hours_converted = [convert(i) for i in range(24)]
    return render_template('index.html',passenger_opt = passenger_options, hour_opt = hours_converted,
                           want_bag_opt = yes_no, want_seat_opt = yes_no, want_meal_opt = yes_no)
    
if __name__ == "__main__":
    app.run(debug=True)  

