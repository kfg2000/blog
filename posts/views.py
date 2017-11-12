from django.shortcuts import render, get_object_or_404, redirect
from .models import Post 
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

    paginator = Paginator(objects, 3) # Show 3 objects per page

    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)
    
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
    form = PostForm(request.POST or None, request.FILES or None)
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
    form = PostForm(request.POST or None, request.FILES or None, instance=item)
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
