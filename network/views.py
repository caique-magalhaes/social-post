import json
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from .models import User , Post , Follower , Following, Post_likes


def index(request):
    
    #Checks if the user is online and leaves a message for the user that only logged-in users will have their likes counted.

    if not request.user.is_authenticated:
        messages.error(request,'The user must be logged in for likes to be counted and for them to follow their favorite users.!!!')

    posts = Post.objects.all().order_by("-date")

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)



    return render(request, "network/index.html",{"page_obj":page_obj})


def new_post(request):

    return render(request, "network/new_post.html")


@csrf_exempt
@login_required
def sent(request):
    """Create a new post"""
    if request.method != "POST":
        return JsonResponse({"error":"POST request required"},status=400)
    
    data = json.loads(request.body)
    
    description = data.get("description","")

    if description == [""]:
        return JsonResponse({"error":"The description is required"})
    
    post = Post(description = description, user = request.user)

    post.save()

    return JsonResponse({"message": "The post was created successfully."}, status=201)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def user_page(request,user_id):
    #get the user that was passed as a parameter.
    user = User.objects.get(id = user_id)
    post = Post.objects.filter(user = user).order_by("-date")

    paginator = Paginator(post, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    followers =  Follower.objects.filter(user = user ).all().count()
    follow_count =  Following.objects.filter(user = user).all().count()

    already_following = False
    
    if request.user.is_authenticated:
        following = Following.objects.filter(user = request.user).all()
        #Checks if the logged-in user is following the user that was passed as a parameter.
        if following is not None:
            for follow in following:
                if follow.following == user:
                    already_following = True
    else:
        #Checks if the user is online and leaves a message for the user that only logged-in users will have their likes counted.
        messages.error(request,'The user must be logged in to leave a "like"!!!')
    

    return render(request, "network/user.html", {"page_obj": page_obj,"user_page":user, "followers":followers, "already_following":already_following, "follow":follow_count})

@csrf_exempt
@login_required
def action_follow(request):
    """ follow a user """
    
    if request.method != "PUT":
        return JsonResponse({"error":"PUT request required"}, status=404)
    
    data = json.loads(request.body)

    following = data["following"]

    if following == "":
        return JsonResponse({"error":"the following is required"})
    

    #adding a potential user to be that you will follow
    add_following = User.objects.filter(username = following).first()

    #Looking in the Following table to see if you already follow the user.
    search_Following = Following.objects.filter(user = request.user).filter(following = add_following)

    #If you don't follow the user, you will be added as following the user and they will receive a follower.
    if not search_Following:
        start_following = Following(user = request.user, following= add_following)
        receive_follower = Follower(user = add_following, follower=request.user )

        start_following.save()
        receive_follower.save()
    
    return HttpResponse({"message": "The user has been successfully updated."},status = 201)


@csrf_exempt
@login_required
def action_unfollow(request):
    """ unfollow a user """
    
    if request.method != "DELETE":
        return JsonResponse({"error":"DELETE request required"}, status=404)
    
    data = json.loads(request.body)

    unfollowing = data["unfollowing"]



    if unfollowing == "":
        return JsonResponse({"error":"the unfollowing is required"})
    
    add_following = User.objects.filter(username = unfollowing).first()
    
    #Check if you already follow the user.
    search_Following = Following.objects.filter(user = request.user).filter(following = add_following)
    receive_follower = Follower.objects.filter(user = add_following).filter(follower=request.user)
    
    #If you already follow the user, then you can unsubscribe and the user will lose the follower.
    if search_Following:
        search_Following.delete()
        receive_follower.delete()

    return HttpResponse({"message": "The user has been successfully updated."},status = 201)



@csrf_exempt
@login_required
def following_page(request):
    #This page only shows the logged-in user the users they follow.

    all_following = Following.objects.filter(user = request.user).all()
    all_posts = []

    for follow in all_following:
        all_posts += Post.objects.filter(user = follow.following)

    
    paginator = Paginator(all_posts, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    

    return render(request, "network/following.html", {"page_obj":page_obj})

@csrf_exempt
@login_required
def edit_post(request):

    """Edit post"""
    if request.method != "PUT":
        return JsonResponse({"error":"PUT request required"},status=400)
    
    data = json.loads(request.body)
    
    post_id = data.get("post_id","")
    description = data.get("description","")

    if description == [""] and post_id == [""]:
        return JsonResponse({"error":"The description and post id  is required"})
    
    post = Post.objects.filter(id=post_id).first()

    #Check if the post being edited belongs to the user; if it doesn't, editing will not be allowed.
    if post.user == request.user:
        post.description = description
        post.save()
        return JsonResponse({"message": "The post was changed successfully.","post_description":post.description})

    else:
        messages.error(request,"You can't change other people's posts, only your own.")
        return JsonResponse({"message": "Forbidden."},status=403)
    



@csrf_exempt
@login_required
def get_like_post(request):
#Retrieving all the posts the user has liked and passing them through a request so that, via JavaScript, it can retrieve them using the GET method and show the user the posts they have already liked.

    show_post = []

    if request.user.is_authenticated:
        post_like = Post_likes.objects.filter(user=request.user).all()

        for post in post_like:
        
            show_post.append(post.post_liked.id)

        """Show Like post"""
        if request.method != "GET":
            return JsonResponse({"error":"GET request required"},status=400)

        return JsonResponse({"post_like":show_post},status=200)
    
@csrf_exempt
@login_required
def sent_like_post(request):

    """update the post in database"""

    #If it's something other than PUT or DELETE, an error will be thrown.
    if request.method != "PUT" and request.method != "DELETE":
        return JsonResponse({"error":"PUT method or DELETE method is required "},status=400)
    
    data = json.loads(request.body)
    
    post_id = data.get("post_id","")


    if post_id == [""]:
        return JsonResponse({"error":"The description and post id is required"})
    
    post = Post.objects.filter(id=post_id).first()

    if request.user.is_authenticated:
        
        #Updating the like count: If the user did not like the post, they are added to the Likes table and the like count in the Posts table is updated. Otherwise, the user is removed from the Likes table and the post is updated, decreasing the like count in the Posts table by 1.

        post_like = Post_likes.objects.filter(user=request.user, post_liked = post).first()

        if post_like:
            post_like.delete()
            post.likes -= 1
            post.save()
            return JsonResponse({"message": "Like a post."},status=201)
        else:
            post_like = Post_likes(user=request.user, post_liked=post)
            post.likes += 1
            post.save()
            post_like.save()
            return JsonResponse({"message":"Remove a like"},status=201)

    else:
        return JsonResponse({"message": "Forbidden."},status=403)


    







