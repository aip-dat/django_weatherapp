from django import forms
from .models import City
import requests

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'City Name'}),
        }

    def clean_name(self):
        city_name = self.cleaned_data['name']
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=afd7cbc5fb7c66ab72fc0c2e62167503'
        response = requests.get(url.format(city_name)).json()
        if response.get('cod') == '404':
            raise forms.ValidationError('City not found. Please enter a valid city name.')
        return city_name
