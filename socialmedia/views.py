from typing import reveal_type

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post, Profile, Comment


@login_required(login_url='/signin')
def home_view(request):
    posts = Post.objects.filter(is_published = True).order_by('-created_at')
    user = request.user
    users = User.objects.filter(is_staff=False, is_superuser=False).exclude(id = user.id)
    d = {
        'posts': posts,
        'users': users
    }
    return render(request, 'index.html', context=d)


def profile_view(request):
    return render(request, 'profile.html')


def signup_view(request):
    somsa = 0
    cool = ''
    if request.method == 'POST':
        print(1)
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username = username).exists():
            somsa = 1
        else:
            if password == confirm_password:
                print(2)
                user = User.objects.create(username=username, password=make_password(password))
                profile = Profile.objects.create(user = user)

                user.save()
                print(username, password, confirm_password)
                return redirect('/signin')
            else:
                messages.error(request, 'Password is not similar !')
                print('Error, password is not match')
    d = {
        'somsa': somsa,
        'cool': cool
    }
    return render(request, 'signup.html', context=d)


def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        auth = authenticate(request, username=username, password=password)

        if auth:
            login(request, auth)
            return redirect('/')
        else:
            # Add an error message if authentication fails
            messages.error(request, "Invalid username or password.")

    return render(request, 'signin.html')


def signout_view(request):
    logout(request)
    return redirect('/signin')


def setting_view(request):
    return render(request, 'setting.html')


def upload_image_view(request):
    if request.method == 'POST':
        profile = request.user.profile
        if 'image' in request.FILES:
            profile.picture = request.FILES['image']
            profile.save()
            return redirect('/setting')
    return render(request, 'upload_image.html')


def post_view(request):
    if request.method == 'POST':

        if 'image' in request.FILES:
            image = request.FILES['image']

        text = request.POST.get('about_post')
        post = Post.objects.create(author = request.user, image = image, text = text )
        post.save()
        return redirect('/')

    return render(request,'index.html')

def comment_view(request, pk):
    if request.method == "POST":
        post = Post.objects.get(id = pk)
        message = request.POST.get('comment')
        author = request.user

        comment = Comment.objects.create(author = author , message = message, post = post)
        comment.save()
        return redirect('/')