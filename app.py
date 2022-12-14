import requests
import json
from flask import Flask, render_template, url_for, request
# from flask_mobility import Mobility
from flask_apscheduler import APScheduler
from dotenv import load_dotenv
load_dotenv()
import os
from getData import updateData

app = Flask(__name__)
# Mobility(app)
scheduler = APScheduler()
branch = os.getenv('branch')

@app.route('/')
def home():
    table_url = f'https://raw.githubusercontent.com/malvabombom/bender-1548/{branch}/data/general.json'
    table = requests.get(table_url).json()
    return render_template('home.html', table=table)

@app.route('/aboutData')
def aboutData():
    return render_template('aboutData.html')

@app.route('/aboutCOVID')
def aboutCOVID():
    return render_template('aboutCOVID.html')

@app.route('/aboutVaccines')
def aboutVaccines():
    return render_template('aboutVaccines.html')

@app.route('/country/<string:country>')
def country(country):
    # print(request.MOBILE)
    data_url = f'https://raw.githubusercontent.com/malvabombom/bender-1548/{branch}/data/time_series/{country}.json'
    data = requests.get(data_url).json()
    return render_template('countryInfo.html', data=data)   


@app.route('/Mexico')
def Mexico():
    table_url = f'https://raw.githubusercontent.com/malvabombom/bender-1548/{branch}/data/mexico/general.json'
    table = requests.get(table_url).json()
    return render_template('homeState.html', table=table)

@app.route('/country/MX/<string:state>')
def state(state):
    # print(request.MOBILE)
    data_url = f'https://raw.githubusercontent.com/malvabombom/bender-1548/{branch}/data/mexico/time_series/{state}.json'
    data = requests.get(data_url).json()
    return render_template('stateInfo.html', data=data)   

@app.route('/test')
def test():
    return render_template('test.html')

def scheduledTask():
    access_token = os.getenv('access_token')
    updateData(access_token)

scheduler.add_job(id='Scheduled task', func=scheduledTask, trigger='cron', timezone='UTC', hour=0, minute=20)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)
