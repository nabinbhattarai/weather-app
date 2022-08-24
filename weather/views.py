from django.shortcuts import render
from django.http import HttpResponse
from .forms import CityForm
from .models import City
import requests

# Create your views here.
def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=#'
    cities = City.objects.all()
    if request.method == 'POST': 
        form = CityForm(request.POST) 
        form.save() 

    form = CityForm()
    weather_data = []
    for city in cities.order_by('id'):
            city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
            
            weather = {
                'city' : city,
                'temperature' : (city_weather['main']['temp']-32)*5/9, 
                'description' : city_weather['weather'][0]['description'],
                'icon' : city_weather['weather'][0]['icon'],
                'wind': city_weather['wind']['speed'],
                'sunrise': city_weather['sys']['sunrise'],
                'sunset': city_weather['sys']['sunset']
            }

            weather_data.append(weather)
        #print(city_weather)

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/home.html', context)