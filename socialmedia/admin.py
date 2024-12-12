from django.contrib import admin

from socialmedia.models import Post, Comment, Profile


# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id',  'author', 'created_at', 'updated_at', 'is_published')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','message')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
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