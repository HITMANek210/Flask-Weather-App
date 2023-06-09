from flask import Flask, request, render_template
import requests
import json

LANG = "en"

api_key = '' #your openweathermap.org API key
url = 'https://api.openweathermap.org/data/2.5/weather?'

app = Flask(__name__)

def weatherInfo(data, countries):
    context = {
        'name' : data['name'],
        'temp' : str(round(data['main']['temp'] - 273.15, 2)) + " °C",
        'feels_like' : str(round(data['main']['feels_like'] - 273.15, 2)) + " °C",
        'temp_min' : str(round(data['main']['temp_min'] - 273.15, 2)) + " °C",
        'temp_max' : str(round(data['main']['temp_max'] - 273.15, 2)) + " °C",
        'pressure' : str(data['main']['pressure']) + " hPa",
        'humidity' : str(data['main']['humidity']) + " %",
        'countries' : countries
    }
    return context
    
@app.route('/',methods=["GET","POST"])
def index():
    countries = json.load(open('countries.json'))

    if request.method == 'POST' and request.form['country'] and request.form['city']:
        country = request.form['country']
        city = request.form['city']
        try:
            new_url = url+'appid={}&q={},{}&lang={}'.format(api_key, str(city), str(country), LANG)
            context = weatherInfo(requests.get(new_url).json(), countries)

            return render_template('index.html', **context)
        except:
            return render_template('index.html', error='error while fetching weather data')
    else:
        new_url = url+'appid={}&q=Warszawa,pl&lang={}'.format(api_key, LANG)
        context = weatherInfo(requests.get(new_url).json(), countries)

        return render_template('index.html', **context)

app.run(debug=True, host="0.0.0.0", port=80)