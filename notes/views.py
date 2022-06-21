from django.shortcuts import render
from django.shortcuts import redirect
from .models import Notes
from .models import User
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user, logout
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json

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
        global current_user
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
    notesList = Notes.objects.order_by('title')
    context = {'latest_Note_list': notesList, 'current_user' : get_user(request)}
    return render(request, 'notes/index.html', context)

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
@csrf_exempt
def bulk_create(request):
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    data = json.loads(request.body.decode('utf-8'))
    print(data)

    limit=data['limit']
    user= User.objects.all().get(id=3)
    for i in range(limit):
        print(i)
    Notes.objects.create(user = get_user(request), title = data['title'], text =data['text']) 
    #Notes.objects.bulk_create()
    return HttpResponse(content= 200)