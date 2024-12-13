from django.urls import path, include
from .views import home_view, profile_view, setting_view, signin_view, signup_view, signout_view, upload_image_view, \
    post_view, comment_view

urlpatterns = [
    path('', home_view),
    path('profile/',profile_view),
    path('setting/', setting_view),
    path('signin/', signin_view),
    path('signup/',signup_view),
    path('signout/', signout_view),
    path('upload_image/', upload_image_view),
    path('post/', post_view),
    path('comment/<int:pk>/', comment_view)
]


