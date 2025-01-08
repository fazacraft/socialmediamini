from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.functional import empty
from django.utils.timezone import now
from .models import Post, Profile, Comment, UserLikePost, UserFollow, Notification


@login_required(login_url='/signin')
def home_view(request):


    user_id = request.user.id
    follow_objects = UserFollow.objects.all()
    black_list = []
    res3 = []
    users = User.objects.filter(is_staff=False, is_superuser=False).exclude(id=user_id)
    noties = Notification.objects.filter(user_accept = request.user)

    for user in follow_objects:
        if user.follower.id == user_id:
            black_list.append(user.following.id)
    for user in users:
        if user.id != 1 and user.id not in black_list:
            res3.append(user)
    res_user = res3

    posts = Post.objects.all().order_by('-created_at')
    post_res = []
    for x in posts:
        if x.author not in res_user:
            post_res.append(x)



    d = {
        'posts': post_res,
        'users': res_user,
        'noties':noties,


    }

    return render(request, 'index.html', context=d)


def profile_view(request):
    return render(request, 'profile.html')


def signup_view(request):
    somsa = 0
    cool = ''
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            somsa = 1
        else:
            if password == confirm_password:

                user = User.objects.create(username=username, password=make_password(password))
                profile = Profile.objects.create(user=user)

                user.save()
                profile.save()

                return redirect('/signin')
            else:
                messages.error(request, 'Password is not similar !')

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


def setting_edit_view(request, pk):
    data = request.POST
    author = User.objects.get(id = pk)

    last_name = data.get('last_name')
    first_name = data.get('first_name')
    email = data.get('email')

    profile = Profile.objects.get(user = author)

    if first_name is not '':
        profile.first_name = first_name
    if last_name is not '':
        profile.last_name = last_name

    if email is not '':
        profile.email = email

    profile.about_me = data.get('about_me')
    profile.save()
    return redirect('/setting')


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
        if request.user.id != post.author_id:
            like_noti = Notification.objects.create(user_act= request.user, user_accept=post.author, type = 1)
            like_noti.save()

        comment = Comment.objects.create(author=author, message=message, post=post)
        comment.save()

        return redirect(f'/#{comment.id}')


def like_view(request):
    post_id = request.GET.get('post_id')
    post = Post.objects.get(pk = post_id)

    author = request.user

    exists = UserLikePost.objects.filter(post_id=post_id, author=author).first()
    like_noti = Notification.objects.filter(user_act=author, user_accept=post.author, type=0)
    if exists:
        exists.delete()
        like_noti.delete()
        return redirect(f'/#{post_id}')


    if author != post.author:
        like_noti =Notification.objects.create(user_act=author, user_accept=post.author, type=0)
        like_noti.save()
    like_obj = UserLikePost.objects.create(post_id=post_id, author=author)
    like_obj.save()
    return redirect(f'/#{post_id}')


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
    user = User.objects.get(id = user_who_following)

    ex = UserFollow.objects.filter(follower = user_who_follower, following_id = user_who_following).first()
    like_noti = Notification.objects.filter(user_act=user_who_follower, user_accept=user, type=2)
    if ex:
        ex.delete()
        like_noti.delete()
        return redirect(f'/profile/?post_author_id={user.profile.id}')

    obj = UserFollow.objects.create(follower = user_who_follower, following_id = user_who_following)
    obj.save()

    if request.user != user:
        like_noti = Notification.objects.create(user_act=user_who_follower, user_accept=user, type=2)
        like_noti.save()

    return redirect(f'/profile/?post_author_id={user.profile.id}')


def follow_from_home_view(request):
    user_who_follower = request.user
    user_who_following = request.GET.get('user_id')
    user = User.objects.get(id = user_who_following)
    ex = UserFollow.objects.filter(follower = user_who_follower, following_id = user_who_following).first()
    like_noti = Notification.objects.filter(user_act=user_who_follower, user_accept=user, type=2)
    if ex:
        ex.delete()
        like_noti.delete()
        return redirect('/')
    obj = UserFollow.objects.create(follower = user_who_follower, following_id = user_who_following)
    obj.save()

    if request.user != user:
        like_noti = Notification.objects.create(user_act=user_who_follower, user_accept=user, type=2)
        like_noti.save()
    return redirect('/')



def profile_view(request):
    post_author_id = request.GET.get('post_author_id')

    authorbek = Profile.objects.get(id = post_author_id)
    followings = UserFollow.objects.filter(follower_id = authorbek.user.id)
    followers = UserFollow.objects.filter(following_id=authorbek.user.id)

    posts = Post.objects.filter(author = Profile.objects.get(id = post_author_id).user)

    d= {
        'posts':posts,
        'author': authorbek,
        'len_posts':len(posts),
        'len_following': len(followings),
        'len_follower': len(followers)
        }

    return render(request, 'profile.html',context=d)


def delete_user_view(request):
    user_id = request.GET.get('user_id')
    user1 =Profile.objects.get(id = user_id).user.username
    delete_user = User.objects.filter(username = user1)
    delete_user.delete()

    return redirect('/')


def search_view(request):

    filter_ = Q(username__icontains = request.POST.get('searchbek'))

    filter_ |= Q(first_name__icontains = request.POST.get('searchbek'))
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
    print(res_user)
    users = User.objects.filter(filter_,is_staff=False).exclude(id = request.user.id)

    d = {
        'users': users,
        'unfollowed_users': res_user
    }
    return render(request, 'search.html', d)

