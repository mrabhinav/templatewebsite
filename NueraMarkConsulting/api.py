from logging import debug
from app import Flask, render_template, request, redirect, url_for
import json
import requests
from werkzeug.wrappers import response
app = Flask(__name__)

@app.route('/languageconverter', methods=['GET', 'POST'])
def langcon():
    given = request.form.get("input")
    url = "https://freekode.centeltech.com/api/minions?txt={}".format(given)
    print(url)
    response = requests.get(url).text
    print(response)
    json_dictionary = json.loads(response)
    print(json_dictionary)
    return render_template ("api.html", output = json_dictionary)

def ktof(ktemp):
    ftemp=(ktemp - 273.15) * 9/5 + 32
    return (ftemp)

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    temp_data = []
    json_dictionary = ""
    if request.method == "POST":
        city = request.form.get("cityasked")
        apikey ="42da01010e33ab054422357fbc10caf0"
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city, apikey)
        response = requests.get(url).text
        json_dictionary = json.loads(response)
        response2 = requests.get(url).content
        print(response2)
        description = json_dictionary["weather"][0]["description"]
        icon = json_dictionary["weather"][0]["icon"]
        icon = "https://openweathermap.org/img/wn/{}@2x.png".format(icon)
        print(icon)
        temp_min = json_dictionary["main"]["temp_min"]
        temp_min = ktof(temp_min)
        temp_min = int("%.0f" %temp_min)
        temp_max = json_dictionary["main"]["temp_max"]
        temp_max = ktof(temp_max)
        temp_max = int("%.0f" %temp_max)
        temp = json_dictionary["main"]["temp"]
        temp = ktof(temp)
        temp = int("%.0f" %temp)
        temp_data = [city, temp_min, temp_max, temp, description]
    return render_template ("weather.html", output = json_dictionary, temp_data = temp_data, icon = icon)
       




if __name__ == "__main__":
    app.run(debug = True)

