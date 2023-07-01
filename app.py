from flask import Flask, render_template, request
from datetime import datetime, time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/submit', methods=['POST'])
def submit():
    airline = request.form.get('airl')
    date_of_journey = request.form.get('date')
    source = request.form.get('src')
    destination = request.form.get('dest')
    # d_time = request.form.get('dep_time')
    # dep_time = datetime.strptime(d_time, '%H:%M').time()
    # a_time = request.form.get('arrival_time')
    # arrival_time = datetime.strptime(a_time, '%H:%M').time()
    # duration = arrival_time-dep_time
    # duration_minutes = (duration.seconds // 60) % 60
    total_stops = request.form.get('stops')
    additional_info = request.form.get('addinf')
    
    output="enjoi"
    return render_template('submit.html', prediction_text=output)

if __name__ == '__main__':
    app.run()
