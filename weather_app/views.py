from django.shortcuts import render
import requests
import datetime




# Create your views here.
def index(req):
    API_KEY = 'cb55ae552f88cc7448f50069bfa10f2b'
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather/?q={}&appid={}&units=metric&lang=hi"
    # forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&cnt=40&lang=hi&appid={}&units=metric"


    if req.method == 'POST':
        city = req.POST['city']

        weather_data, daily_forecasts = get_weather_forecast(city, API_KEY, current_weather_url, forecast_url)

        context = {
            'weather_data1': weather_data,
            'daily_forecasts1': daily_forecasts,
        }

        return render(req, 'weather_app/index.html', context)

    else:
        return render(req,'weather_app/index.html')



def get_weather_forecast(city,api_key,curr_url,forecast_url):
    response = requests.get(curr_url.format(city,api_key)).json()
    latitude = response['coord']['lat']
    longitute = response['coord']['lon']


    # forecasting response
    forecast_res = requests.get(forecast_url.format(latitude,longitute,api_key)).json()

    weather_data = { # dictionary that would pass as parameter to our template
        "city":city,
        "temperature":round(response["main"]["temp"],2),
        "description":response["weather"][0]["description"],
        "icon":response['weather'][0]['icon']
    }   

    engTohindDays = {
        "Monday":"सोम",
        "Tuesday":"मंगल",
        "Wednesday":"बुध",
        "Thursday":"गुरु",
        "Friday":"शुक्र",
        "Saturday":"शनि",
        "Sunday":"रवि"
    }

    daily_forecasts = []
    # for daily_data in forecast_res['daily'][:5]:
    #     daily_forecasts.append({
    #         'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
    #         'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
    #         'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
    #         'description': daily_data['weather'][0]['description'],
    #         'icon': daily_data['weather'][0]['icon'],
    #     })


    myInput = forecast_res["list"]
    for i in range(0,len(myInput),8):
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(myInput[i]['dt']).strftime('%A'),
            'day_in_hindi': engTohindDays[datetime.datetime.fromtimestamp(myInput[i]['dt']).strftime('%A')],
            'min_temp': round(myInput[i]['main']['temp_min'], 2),
            'max_temp': round(myInput[i]['main']['temp_max'], 2),
            'avg_temp':round((myInput[i]['main']['temp_min'] + myInput[i]['main']['temp_max'])/2,2),
            'description': myInput[i]['weather'][0]['description'],
            'icon': myInput[i]['weather'][0]['icon'],
        })
        

    return weather_data,daily_forecasts
