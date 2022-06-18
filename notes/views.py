from django.shortcuts import render
from django.shortcuts import redirect
from .models import Notes
from .models import New_user

from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


"""
index : display notes by time
detail : retreive the note object, then edit
Now in your time on the web you may have come across such beauties as ME2/Sites/dirmod.htm?sid=&type=gen&mod=Core+Pages&gid=A6CD4967199A42D9B65B1B. You will be pleased to know that Django allows us much more elegant URL patterns than that.
To get from a URL to a view, Django uses what are known as ‘URLconfs’. A URLconf maps URL patterns to views.

https://docs.djangoproject.com/en/4.0/topics/db/queries/
"""

user=None
def signup_new(request):
    return render(request,'notes/signup.html')

def signup(request):
    New_user.objects.create(user_id = request.POST['user_id'],user_pwd=request.POST['user_pwd'])
    return redirect('index')

def login(request):
    global user
    uid= request.POST['user_id']
    upwd = request.POST['user_pwd']
    try:
        if New_user.objects.filter(user_id = uid).get(user_pwd=upwd):
            print("logged in")
            user= New_user.objects.get(user_id = uid)
            return redirect('index')
        else:
            print("no")
    except New_user.DoesNotExist:
        raise Http404("Note does not exist")

def logout(request):
    global user
    user=None
    return redirect('index')


#get
def index(request):
    global user
    notesList = Notes.objects.order_by('title')
    context = {'latest_Note_list': notesList, 'current_user' : user}
    return render(request, 'notes/index.html', context)

#get
def detail(request, note_id):
    try:
        note = Notes.objects.get(pk=note_id)
    except Notes.DoesNotExist:
        raise Http404("Note does not exist")
    return render(request, 'notes/detail.html', {'notes': note, 'current_user':user})

#get
def new(request):
    return render(request, 'notes/new.html')

#post
def create(request):
    note = Notes.objects.create(user=user,title = request.POST.get('note_title'),text=request.POST.get('note_text'))
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