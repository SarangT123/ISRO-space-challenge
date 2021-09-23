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


@views.route('/')
def home():
    return render_template('ipcheck.html')


@views.route('/ip/<ip>')
def ip(ip):
    url = f'http://ip-api.com/json/{ip}'
    r = requests.get(url)
    j = json.loads(r.text)
    session['city'] = j['city']
    return redirect(f"/{j['lat']}/{j['lon']}")


@views.route('/<lan>/<lon>', methods=['POST', 'GET'])
def weather(lan, lon):
    if request.method == 'POST':
        print(request.form['loc'])
        return redirect(f"{HOST}/{request.form['loc']}")
    else:
        print(type(lan), lon)
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/onecall?lat={float(lan)}&lon={float(lon)}&exclude=hourly,daily&appid={token}")
        info = json.loads(r.text)
        main = info["current"]["weather"][0]["main"]
        desc = info["current"]["weather"][0]["description"]
        print(main, desc)
        #
        #
        #
        if "city" in session:
            moreinfo = [f"Location : {session['city']}", f"latittude : {info['lat']}",
                        f"lontittude : {info['lon']}",
                        f"timezone : {info['timezone']}",
                        f"temp : {info['current']['temp']}",
                        f"pressure : {info['current']['pressure']}",
                        f"humidity : {info['current']['humidity']}",
                        f"wind speed : {info['current']['wind_speed']}"]
            session.pop('city')
        else:
            moreinfo = [f"latittude : {info['lat']}",
                        f"lontittude : {info['lon']}",
                        f"timezone : {info['timezone']}",
                        f"temp : {info['current']['temp']}",
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
        return render_template("data.html", main=main, desc=desc, info=moreinfo)
