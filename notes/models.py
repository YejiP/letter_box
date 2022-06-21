from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

#https://docs.djangoproject.com/en/4.0/topics/auth/default/ 이거 사용해서 다시

class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.title

