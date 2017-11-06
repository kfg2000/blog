from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post 

def post_home(request):
	context = {
		'title': 'The Posts'
	}
	return render(request, 'home.html', context)

def main_post(request):
	context = {
		'headline': 'OMG'
	}
	return render(request, 'top.html', context)

def fun(request):
	context = {
		'funnyposts': 'HAHA'
	}
	return render(request, 'fun.html', context)

def post_list(request):
	objects = Post.objects.all()
	context = {
		"list": objects
	}
	return render(request, 'list.html', context)

def post_detail(request, post_id):
	# way 1: item = Post.objects.get(id=1), way 2:
	item = get_object_or_404(Post, id = post_id)
	context = {
		'item': item,
	}
	return render(request, 'detail.html', context)