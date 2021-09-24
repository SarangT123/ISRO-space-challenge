import asyncio
from flask import Flask, session, Blueprint, render_template, redirect, url_for, request
import requests
import json
import subprocess
from matplotlib import pyplot as plt


def Graph(datax, datay, title, xl, yl):
    x = datax
    y = datay
    fig = plt.figure(figsize=(10, 5))
    plt.rcParams['axes.facecolor'] = '#fcb86a'
    plt.rcParams['text.color'] = 'black'
    plt.rcParams['axes.labelcolor'] = 'black'
    fig.patch.set_facecolor('#fcb86a')
    plt.plot(x, y, color='#6a9bfc')
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.title(title)
    plt.savefig('website/static/mygraphl.png')


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

@forecast.route('/forecast/<city>', methods=['POST','GET'])
def city(city):
    if request.method == "POST":
        return redirect(f"https://ISRO-space-challenge.c3tmlive.repl.co/forecast/{request.form['loc']}")
    data = forecast_week(city)
    if data[0] == "":
        return "<h1>Your city isnt available on our databse yet</h1>"
    print("data",data)
    weather = data[2].split('#')
    weather.pop(0)
    weather[-1] = weather[-1].replace("\n", "")
    print(weather ,"replaced")
    temp = data[1].split('#')
    temp.pop(0)
    temp[-1] = temp[-1].replace("\n", "")
    dates = data[0].split('#')
    dates.pop(0)
    dates[-1] = dates[-1].replace("\n", "")
    print(weather,dates,temp)
    graphdate = []
    for i in range(len(temp)):
        graphdate.append(dates[i].split(' ')[0])
    print(len(temp), len(graphdate))
    Graph(graphdate,temp,"Temparature graph", "Dates", "Temparature in celcius")
    return render_template('forecast.html', main=graphdate,weather=weather,temp=temp)

@forecast.route('/ip/forecast/<ip>')
def ip(ip):
    url = f'http://ip-api.com/json/{ip}'
    r = requests.get(url)
    j = json.loads(r.text)
    session['city'] = j['city']
    return redirect(f"/forecast/{j['city']}")
