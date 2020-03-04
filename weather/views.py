from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
	appid = 'da5a90f95e765bcf192e252f8fd995a6'
	url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
	context = {'error': False}

	if(request.method == 'POST'):
		if not City.objects.filter(name__iexact=request.POST['name']):
			form = CityForm(request.POST)
			form.save()
		else:
			context = {'error': True}

	form = CityForm()

	cities = City.objects.all()
	all_cities = []

	for city in cities:
		res = requests.get(url.format(city.name)).json()
		city_info = {
			'city': city.name,
			'temp': res["main"]["temp"],
			'icon': res["weather"][0]["icon"],
		}

		all_cities.append(city_info)

	context['all_info'] = all_cities
	context['form'] = form 

	return render(request, 'weather/index.html', context)
