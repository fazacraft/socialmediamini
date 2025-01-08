from django.contrib import admin
from django.contrib.auth.models import User

from socialmedia.models import Post, Comment, Profile, UserLikePost, UserFollow, Notification


# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id',  'author', 'created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','message')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'last_name', 'first_name', 'email', 'created_at', 'updated_at')

@admin.register(UserLikePost)
class UserLikePostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post')

@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'created_at','following')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_act', 'type','created_at','user_accept')



# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#
# @admin.register(Hashtag)
# class HashtagAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'first_name')