from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Like
from .forms import PostForm, UserSignup, UserLogin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote 
from django.http import Http404, JsonResponse
from django.utils import timezone 
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

def usersignup(request):
    context = {}
    form = UserSignup()
    context['form'] = form
    
    if request.method == 'POST':
        form = UserSignup(request.POST)
        if form.is_valid():
            user = form.save()
            x = user.username
            y = user.password

            user.set_password(y)
            user.save()

            auth = authenticate(username=x,password=y)
            login(request, auth)

            return redirect("posts:list")
        
        messages.warning(request, form.errors)
        return redirect("posts:signup")
    return render(request, 'signup.html', context)

def userlogin(request):
    context = {}
    form = UserLogin()
    context['form'] = form
    
    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():
            user_user = form.cleaned_data['username']
            user_pass = form.cleaned_data['password']

            auth = authenticate(username=user_user, password=user_pass)
            if auth is not None:
                login(request, auth)
                return redirect("posts:list")
            messages.warning(request, 'Incorrect user/pass...')
            redirect("posts:login")
        messages.warning(request, form.errors)
        return redirect("posts:login")
    return render(request, 'login.html', context)

def userlogout(request):
    logout(request)
    return redirect("posts:list")


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
    
    today = timezone.now().date()

    objects = Post.objects.filter(draft=False, publish_date__lte=today)
    if request.user.is_staff:
        objects = Post.objects.all()

    query = request.GET.get("q")
    if query:
        objects = objects.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(author__first_name__icontains=query)|
            Q(author__last_name__icontains=query)
            ).distinct()

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
        "list": objects,
        "today": today,
    }
    return render(request, 'list.html', context)

def post_detail(request, post_slug):
    # way 1: item = Post.objects.get(id=1), way 2:
    item = get_object_or_404(Post, slug = post_slug)
    if not request.user.is_staff and (item.draft or item.publish_date > timezone.now().date()):
        raise Http404

    liked = False
    if request.user.is_authenticated():
        if Like.objects.filter(post=item, user=request.user).exists():
            liked = True
        else:
            liked = False


    like_count = item.like_set.count()

    context = {
        'item': item,
        'liked': liked,
        'like_count': like_count,
    }
    return render(request, 'detail.html', context)

def post_create(request):
    if not request.user.is_staff:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Awesome, you added a post :)")
        return redirect("posts:list")
    context = {
    'form': form,
    }
    return render(request, 'post_create.html', context)

def post_update(request, post_slug):
    if not request.user.is_staff:
        raise Http404
    item = Post.objects.get(slug=post_slug)
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

def post_delete(request, post_slug):
    if not request.user.is_staff:
        raise Http404
    Post.objects.get(slug=post_slug).delete()
    messages.warning(request, "You sure?")
    return redirect("posts:list")

def like_button(request, post_id):
    post_object = Post.objects.get(id=post_id)

    like, created = Like.objects.get_or_create(user=request.user, post=post_object)

    if created:
        action = "like"
    else:
        like.delete()
        action = "unlike"

    like_count = post_object.like_set.count()
    response = {
        'action':action,
        'like_count': like_count,
    }
    return JsonResponse(response, safe=False)