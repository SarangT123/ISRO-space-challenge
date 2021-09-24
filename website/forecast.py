import asyncio
from flask import Flask, session, Blueprint, render_template, redirect, url_for, request
import requests
import json
import subprocess



forecast = Blueprint('forecast', __name__)
@forecast.route('/forecast')
def home():
    return render_template('ipforecast.html')

def forecast_week(city):
    x = subprocess.run(['python3', 'weather_forecast.py','0',city], stdout=subprocess.PIPE)
    x =x.stdout.decode('utf-8')
    y = subprocess.run(['python3', 'weather_forecast.py','1',city], stdout=subprocess.PIPE)
    y =y.stdout.decode('utf-8')
    z = subprocess.run(['python3', 'weather_forecast.py','2',city], stdout=subprocess.PIPE)
    z =z.stdout.decode('utf-8')

    return [x,y,z]

@forecast.route('/api/forecast')
def apif():
    return forecast_week()

@forecast.route('/forecast/<city>')
def city(city):
    data = forecast_week(city)
    print("data",data)
    weather = data[2].split('#') 
    temp = data[1].split('#')
    dates = data[0].split('#')
    print(weather,dates,temp)
    return render_template('forecast.html', main=dates,weather=weather,temp=temp)

@forecast.route('/ip/forecast/<ip>')
def ip(ip):
    url = f'http://ip-api.com/json/{ip}'
    r = requests.get(url)
    j = json.loads(r.text)
    session['city'] = j['city']
    return redirect(f"/forecast/{j['city']}")
