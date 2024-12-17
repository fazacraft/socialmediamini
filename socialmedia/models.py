from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    image = models.ImageField(upload_to='posts/')
    text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def likes_count(self):
        return self.likes.count() -1

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
    following = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.follower.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(upload_to='profiles/', default='nonegigachad.webp')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
