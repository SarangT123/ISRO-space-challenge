from flask import Flask, session, Blueprint, render_template, redirect, url_for, Response, request
import requests
import os
import json
from dotenv import load_dotenv
from matplotlib import pyplot as plt
load_dotenv()
token = os.getenv("keyid")
views = Blueprint('views', __name__)

HOST = "https://ISRO-space-challenge.c3tmlive.repl.co"


def barGraph(datax, datay, title, xl, yl):
    x = datax
    y = datay
    fig = plt.figure(figsize=(10, 5))
    plt.rcParams['axes.facecolor'] = '#fcb86a'
    plt.rcParams['text.color'] = 'black'
    plt.rcParams['axes.labelcolor'] = 'black'
    fig.patch.set_facecolor('#fcb86a')
    plt.bar(x, y, color='#6a9bfc',
            width=0.4,)
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.title(title)
    plt.savefig('website/static/mygraph.png')


@views.route('/weather')
def home():
    return render_template('ipcheck.html')
@views.route('/')
def main():
    return render_template('land.html')

@views.route('/ip/<ip>')
def ip(ip):
    url = f'http://ip-api.com/json/{ip}'
    r = requests.get(url)
    j = json.loads(r.text)
    session['city'] = j['city']
    print(j['city'],ip)
    return redirect(f"/{j['lat']}/{j['lon']}/{j['city']}")


@views.route('/<lan>/<lon>/<location>', methods=['POST', 'GET'])
@views.route('/<lan>/<lon>', methods=['POST', 'GET'])
def weather_phone(lan, lon,location="NA"):
    if request.method == 'POST':
        r = requests.get(f"https://nominatim.openstreetmap.org/search?q={request.form['loc']}&format=json")
        print(r.text)
        r = json.loads(r.text)
        print(r)
        try:
            lat = r[0]['lat']
            lon = r[0]['lon']
        except:
            return render_template('500notindb.html')
        return redirect(f'/{lat}/{lon}/{request.form["loc"]}')
            
    else:
        print(type(lan), lon)
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/onecall?lat={float(lan)}&lon={float(lon)}&exclude=hourly,daily&appid={token}")
        info = json.loads(r.text)
        print(info)
        main = info["current"]["weather"][0]["main"]
        desc = info["current"]["weather"][0]["description"]
        print(main, desc)
        #
        #
        #
        if "city" in session:
            moreinfo = [f"Location : {session['city']}", f"latitude : {info['lat']}",
                        f"longitude : {info['lon']}",
                        f"timezone : {info['timezone']}",
                        f"temperature (Kelvin) : {info['current']['temp']}",
                        f"pressure : {info['current']['pressure']}",
                        f"humidity : {info['current']['humidity']}",
                        f"wind speed : {info['current']['wind_speed']}"]
            session.pop('city')
        else:
            moreinfo = [f"latitude : {info['lat']}",
                        f"longitude : {info['lon']}",
                        f"timezone : {info['timezone']}",
                        f"temperature (Kelvin) : {info['current']['temp']}",
                        f"pressure : {info['current']['pressure']}",
                        f"humidity : {info['current']['humidity']}",
                        f"wind speed : {info['current']['wind_speed']}"]

            #
        #
        #
        y = [info['current']['temp'], info['current']['pressure'],
             info['current']['humidity'], info['current']['wind_speed']]
        x = ["temp", "pressure", "humidity", "wind speed"]

        barGraph(x, y, "Information in a single graph", "Items", "Value")
        return render_template("data.html", main=main, desc=desc, info=moreinfo, loc = location)

