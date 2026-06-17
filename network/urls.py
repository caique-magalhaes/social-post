
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post",views.new_post, name="new_post"),
    path("user_page/<str:user_id>",views.user_page, name="user_page"),
    path("following", views.following_page, name="following_page"),

    #API ROUTE
    path("post/sent",views.sent, name="sent"),
    path("follow",views.action_follow, name="follow"),
    path("unfollow",views.action_unfollow, name="unfollow"),
    path("post/edit/",views.edit_post, name="edit" ),
    path("post/get-like/",views.get_like_post, name="get_post"),
    path("post/like", views.sent_like_post, name="like")
]
