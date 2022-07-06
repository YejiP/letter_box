from django.shortcuts import render
from django.shortcuts import redirect
from requests import session
from .models import Notes
from .models import User
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user, logout
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
import pika
"""
index : display notes by time
detail : retreive the note object, then edit
Now in your time on the web you may have come across such beauties as ME2/Sites/dirmod.htm?sid=&type=gen&mod=Core+Pages&gid=A6CD4967199A42D9B65B1B. You will be pleased to know that Django allows us much more elegant URL patterns than that.
To get from a URL to a view, Django uses what are known as ‘URLconfs’. A URLconf maps URL patterns to views.

https://docs.djangoproject.com/en/4.0/topics/db/queries/
"""


current_user=None

def signup_new(request):
    return render(request,'notes/signup.html')

def signup(request):
    User.objects.create_user(username = request.POST['user_id'],password=request.POST['user_pwd'],last_login=timezone.now(),is_superuser=True)
    return redirect('index')

def login_view(request):
    #signup 에서 create_user 아니라 create 써서 error나는 거였다.
    username= request.POST['user_id']
    password = request.POST['user_pwd']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('index')
    else:
        # Return an 'invalid login' error message.
        raise Http404("invalid login")

        

def logout_view(request):
    logout(request)
    return redirect('index')


#get
def index(request):
    notesList = Notes.objects.order_by('created_at')
    context = {'latest_Note_list': notesList, 'current_user' :get_user(request)}
    return render(request, 'notes/index.html',context)

#get
def detail(request, note_id):
    try:
        note = Notes.objects.get(pk=note_id)
    except Notes.DoesNotExist:
        raise Http404("Note does not exist")
    return render(request, 'notes/detail.html', {'notes': note, 'current_user':get_user(request)})

#get
def new(request):
    return render(request, 'notes/new.html')

#post
def create(request):
    #나중에 삭제 user! user= User.objects.all().get(id=3)
    note = Notes.objects.create(user=get_user(request),title = request.POST.get('note_title'),text=request.POST.get('note_text'))
    return render(request, 'notes/detail.html', {'notes': note})

#form
def edit(request,note_id):
    note = Notes.objects.get(pk=note_id)
    return render(request, 'notes/edit.html',{'notes': note})

#put or patch
def update(request,note_id):
        note=Notes.objects.get(pk=note_id)
        note.title = request.POST.get("title")
        note.text = request.POST.get("text")
        note.save()
        return render(request, 'notes/detail.html', {'notes': note})

#delete
def delete(request, note_id):
    try:
        Notes.objects.filter(pk=note_id).delete()
    except Notes.DoesNotExist:
        raise Http404("Note does not exist")
    notesList = Notes.objects.order_by('title')
    return redirect('index')
    


#post endpoint, and create HttpResponse notes, limit is the number of notes.
#I cannot call request.post/get together in the same endpoint.
##10000명이 동시에 note create -> 빨리만드려고??????1초안ㅇㅔ

"""
Rubber duck
what am i doing?
: I am going to use Rabbitmq to implement bulk_create

why do i use rabbitmq?
: because we assumed that the memory is limited in this app, so not to face memory issue
and then wanted to work asynchronously???

how do i use it...
: Instad of using array in code, use sender, receiver to process ....?

"""


# @csrf_exempt
# def bulk_create(request):
#     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
#     data = json.loads(request.body.decode('utf-8'))

#     limit=data['limit']

#     #bulk way
#     user = User.objects.all().get(pk=3)

#     #Establish a connection
#     connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
#     channel = connection.channel()
    
#     channel.queue_declare(queue='notes')
#     #sender should be in here, where notes are created.
#     for i in range(1):
#         message ={'user' : user.username,  'title' : data['title'] , 'text' : data['text']}
#         channel.basic_publish(exchange='',
#                       routing_key='notes',
#                       body= json.dumps(message))
    
#     #receiver should be around here??? in the same function?? then #132 as soon as note is created, it will process 
#     #even though notes are still generated.

#     def callback(ch, method, properties, body):
#         mesage=json.loads(body)
#         Notes.objects.create(user =mesage['user'], title = mesage['title'], text =mesage['text']) 

#     channel.basic_consume(queue='notes',
#                       auto_ack=True,
#                       on_message_callback=callback)
    
#     channel.start_consuming()

#     return HttpResponse(content= 200)
