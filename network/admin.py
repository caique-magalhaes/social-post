from django.contrib import admin
from network.models import Post, Follower, Following, Post_likes

class Post_Admin(admin.ModelAdmin):
    list_display = ("id","user","description","date")
    search_fields = ("user",)
    list_filter = ("user","date")

class Follower_Admin(admin.ModelAdmin):
     list_display = ("user","follower")

class Following_Admin(admin.ModelAdmin):
     list_display = ("user","following")

class Post_likes_admin(admin.ModelAdmin):
     list_display= ("user","post_liked")



admin.site.register(Post, Post_Admin),
admin.site.register(Follower, Follower_Admin),
admin.site.register(Following, Following_Admin),
admin.site.register(Post_likes, Post_likes_admin)