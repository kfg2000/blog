from django.shortcuts import render
import requests
from django.http import JsonResponse

def place_text_search(request):
	key = "AIzaSyD6G16oxVKBsaLs6Ro1c3iaCItkBMDSIOc"
	query = "coded"
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&region=kw&key=%s"%(query, key)

	response = requests.get(url)

	lists = response.json().get('results')
	
	context = {
	'name': lists
	}
	return render(request, 'test.html', context)
	#return JsonResponse(response.json(), safe=False)
