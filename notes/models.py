from tkinter import CASCADE
from django.db import models

#https://docs.djangoproject.com/en/4.0/topics/auth/default/ 이거 사용해서 다시
class New_user(models.Model):
    user_id = models.CharField(max_length=10)
    user_pwd = models.CharField(max_length=10) 
    def __str__(self):
        return self.user_id

class Notes(models.Model):
    user = models.ForeignKey(New_user,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.title

