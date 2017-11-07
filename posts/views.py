from django.shortcuts import render, get_object_or_404, redirect
from .models import Post 
from .forms import PostForm
from django.contrib import messages

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

def post_create(request):
	form = PostForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, "Awesome, you added a post :)")
		return redirect("posts:list")
	context = {
	'form': form,
	}
	return render(request, 'post_create.html', context)

def post_update(request, post_id):
	item = Post.objects.get(id=post_id)
	form = PostForm(request.POST or None, instance=item)
	if form.is_valid():
		form.save()
		messages.info(request, "Updated")
		return redirect("posts:list")
	context = {
	'form': form,
	'item': item,
	}
	return render(request, 'post_update.html', context)

def post_delete(request, post_id):
	Post.objects.get(id=post_id).delete()
	messages.warning(request, "You sure?")
	return redirect("posts:list")
