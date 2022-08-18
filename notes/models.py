from asyncore import read
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from psycopg2 import Timestamp


class App_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_active_time = models.DateTimeField()

    def __str__(self):
        return self.last_active_time


class Notes(models.Model):
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver')
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=500)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Audit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model_type = models.CharField(max_length=20)
    data = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)


class Friend_request(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='to_user')


class Friendship(models.Model):
    me = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='me')
    my_friend = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='my_friend')
