from django.db import models
from django.contrib.auth.models import User # Default user model of django

import datetime
from django.utils.timezone import utc

now = datetime.datetime.utcnow().replace(tzinfo=utc)

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Each room can have max one topic but if topic is deleted room can not.
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True) 
    # related_name because we already have an user in host 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # id = 
    outside_review = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.description[:20]
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Each message can have max one room, when room is deleted message also.
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]
    
    class Meta:
        ordering = ['-updated', '-created']
    
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")