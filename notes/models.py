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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Audit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model_type = models.CharField(max_length=20)
    data = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)

    # ideal : i would like to put 'Notes.object.create()???'
    # i cannot use array,, yeah maybe array issue.. bulk_insert(array) => overloading...? bulk_insert(obj,times)
    # postgres : insert redundant data at once.

    """

    approach1.. 
    problem 1 : Array
    problem 2 : overriding django method => never override!!! Monkey patch..? bad idea!
    problem 3 : Insert vs bulk inserting in postgres => (?_?)
    1. i am putting down other django developers
    2. my bulk create does 1 sql query, i proved... bulk create without using array...?
    what am i doing rn, why am i doing this.. type..
 
    approach2..
    you execute sql command
    problem 1 : 100k 25s -> 100 k records -> 100 k insert command insert 1record

    1query will insert 100k records at once, and it takes 25s, 
    1query will insert 20k records at once, 5s => 병렬적으로 처리돼서 기다릴 필요없이 5초에 된다! concurrently ..! 패럴럴 동시에~

    INSERT INTO TABLE VALUES(,,,) One query, values can have multiple records
    problem 4 : how do we get 500k records get in fast..?
    """
