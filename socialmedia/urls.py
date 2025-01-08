from django.urls import path, include
from .views import home_view, profile_view, setting_view, signin_view, signup_view, signout_view, upload_image_view, \
    post_view, comment_view, like_view, delete_post_view, follow_view, delete_user_view, search_view, setting_edit_view,follow_from_home_view

urlpatterns = [
    path('', home_view),
    path('profile/',profile_view),
    path('setting/', setting_view),
    path('signin/', signin_view),
    path('signup/',signup_view),
    path('signout/', signout_view),
    path('upload_image/', upload_image_view),
    path('post/', post_view),
    path('comment/<int:pk>/', comment_view),
    path('like/',like_view),
    path('delete_post/', delete_post_view),
    path('follow/', follow_view),
    path('delete_user/', delete_user_view),
    path('search/', search_view),
    path('setedit/<int:pk>/',setting_edit_view),
    path('follow_from_home/',follow_from_home_view)

]


