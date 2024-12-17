from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Post, Profile, Comment, UserLikePost, UserFollow


@login_required(login_url='/signin')
def home_view(request):


    user_id = request.user.id
    follow_objects = UserFollow.objects.all()
    black_list = []
    res3 = []
    users = User.objects.filter(is_staff=False, is_superuser=False).exclude(id=user_id)
    for user in follow_objects:
        if user.follower.id == user_id:
            black_list.append(user.following.id)
    for user in users:
        if user.id != 1 and user.id not in black_list:
            res3.append(user)
    res_user = res3
    for x in follow_objects:
        print('=' * 50)
        print(x.follower.id)
        print(x.following.id)
        print('='*50)
    posts = Post.objects.all().order_by('-created_at')
    post_res = []
    for x in posts:
        if x.author not in res_user:
            post_res.append(x)
    print(post_res)
    d = {
        'posts': post_res,
        'users': res_user,

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

        if User.objects.filter(username=username).exists():
            somsa = 1
        else:
            if password == confirm_password:
                print(2)
                user = User.objects.create(username=username, password=make_password(password))
                profile = Profile.objects.create(user=user)

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
        post = Post.objects.create(author=request.user, image=image, text=text)
        post.save()
        return redirect('/')

    return render(request, 'index.html')


def comment_view(request, pk):
    if request.method == "POST":
        post = Post.objects.get(id=pk)
        message = request.POST.get('comment')
        author = request.user

        comment = Comment.objects.create(author=author, message=message, post=post)
        comment.save()

        return redirect('/')


def like_view(request):
    post_id = request.GET.get('post_id')
    author = request.user
    exists = UserLikePost.objects.filter(post_id=post_id, author=author).first()
    if exists:
        exists.delete()
        return redirect('/')

    like_obj = UserLikePost.objects.create(post_id=post_id, author=author)
    like_obj.save()
    return redirect('/')


def delete_post_view(request):
    data = request.GET.get('post_id')
    author = request.user
    qyu = Post.objects.filter(id = data, author = author).exists()
    if qyu:
        Post.objects.filter(id=data, author=author).delete()
    return redirect('/')





def follow_view(request):
    user_who_follower = request.user
    user_who_following = request.GET.get('user_id')
    obj = UserFollow.objects.create(follower = user_who_follower, following_id = user_who_following)
    obj.save()

    return redirect('/')



def profile_view(request):
    post_author_id = request.GET.get('post_author_id')
    authorbek = Profile.objects.get(id = post_author_id)
    print(authorbek.user.username)
    print(post_author_id)
    posts = Post.objects.filter(author = Profile.objects.get(id = post_author_id).user)
    print(posts)

    d= {
        'posts':posts,
        'author': authorbek,
        'len_posts':len(posts)
    }
    return render(request, 'profile.html',context=d)






# def add_comments_to_posts(posts):
#     return list(map(filter_comments, posts))
#
# def filter_comments(post):
#     post.comments = Comment.objects.filter(post_id = post.id)
#     return post
