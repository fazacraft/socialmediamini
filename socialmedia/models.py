from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User

NOTIFICATION_TYPE = (
    (0, "Like"),
    (1, "Comment"),
    (2, "Follow"),
)


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    image = models.ImageField(upload_to='posts/')
    text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.author.username

    def comments_count(self):
        return self.comments.count()

    def like_username(self):
        return self.author_like.username


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    message = models.CharField(max_length=128)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.author.username


class UserLikePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post.author.username


class UserFollow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.follower.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(upload_to='profiles/', default='nonegigachad.webp')
    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    about_me = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def following_count(self):
        return UserFollow.objects.filter(following_id=self.user.id).count()


class Notification(models.Model):
    user_act = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_act')
    type = models.IntegerField(default=0, choices=NOTIFICATION_TYPE)
    user_accept = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_accept')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
