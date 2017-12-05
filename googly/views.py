from django.shortcuts import render
import requests
from django.http import JsonResponse

def place_text_search(request):
	key = "AIzaSyD6G16oxVKBsaLs6Ro1c3iaCItkBMDSIOc"
	query = request.GET.get('query','coded')
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&region=kw&key=%s"%(query, key)

	next_page = request.GET.get('nextpage')
	if next_page is not None:
		url += "&pagetoken="+next_page

	response = requests.get(url)

	lists = response.json()
	
	context = {
	'name': lists
	}
	return render(request, 'place_list.html', context)
	#return JsonResponse(response.json(), safe=False)

def place_detail(request):
	key = "AIzaSyD6G16oxVKBsaLs6Ro1c3iaCItkBMDSIOc"
	place_id = request.GET.get('place_id','')
	url = 'https://maps.googleapis.com/maps/api/place/details/json?key=%s&placeid=%s'%(key,place_id)
	mapkey = "AIzaSyBB_kQkHubIBnM3s6KEpabGYDVDZ3P8gTk"

	response = requests.get(url)

	context = {
	'response': response.json(),
	'map': mapkey,
	}
	return render(request,"place_detail.html", context)
	#return JsonResponse(response.json(), safe=False)