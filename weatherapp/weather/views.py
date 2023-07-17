import requests
from requests.exceptions import RequestException
from .forms import CityForm
from .models import City
from django.shortcuts import render
from django.http import HttpResponseServerError

def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=afd7cbc5fb7c66ab72fc0c2e62167503'
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            weather_data = get_weather_data(city_name)
            if weather_data is not None:
                form.save()
            else:
                # Handle city not found case
                # For example, you can display an error message or redirect back to the form with an error
                error_message = 'City not found.'
                return render(request, 'weather/weather.html', {'form': form, 'error_message': error_message})
    else:
        form = CityForm()
    
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        city_weather = get_weather_data(city.name)
        if city_weather is not None:
            weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/weather.html', context)


def get_weather_data(city_name):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=afd7cbc5fb7c66ab72fc0c2e62167503'
    r = requests.get(url.format(city_name)).json()
    if r['cod'] == '404':
        return None
    city_weather = {
        'city': city_name,
        'temperature' : r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }
    return city_weather