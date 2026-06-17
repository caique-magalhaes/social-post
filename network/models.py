from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser,models.Model):
    pass

class Post(models.Model):
    description = models.TextField(max_length=500, blank=False, null=False)
    date = models.DateTimeField(default=datetime.now, blank=False)
    likes = models.IntegerField(default=0)
    user= models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="posts"
    )

    def __str__(self):
        return f'{self.user.username} - {self.description}'
    

class Follower(models.Model):
     user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="user_followers"
         
     )
     follower = models.ForeignKey(
         to = User,
         on_delete=models.CASCADE,
         related_name="follower",
         null=True,
         blank=True
     )
   

class Following(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user_follows"
         
     )
    following = models.ForeignKey(
         to = User,
         on_delete=models.CASCADE,
         related_name="following",
         null=True,
         blank=True
)
    
class Post_likes(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="user_liked")
    
    post_liked = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="post",
        null=False,
        blank=False
    )

    

    