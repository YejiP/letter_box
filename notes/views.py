import pwd
from django.shortcuts import render
from django.shortcuts import redirect
from .tasks import async_note_create
from .models import Notes
from .models import User
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user, logout
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from .emit_event import Emit_event
from datetime import datetime, timezone
from django.core.paginator import Paginator
from .form import SignUpForm

current_user = None


def signup_new(request):
    regForm = SignUpForm()
    return render(request, 'notes/signup.html', {'regForm': regForm})


def signup(request):
    # if request.method == 'POST':
    regForm = SignUpForm(request.POST)  # form needs content
    if regForm.is_valid():
        timestamp = datetime.now(timezone.utc)
        username = request.POST['username']
        password = request.POST['password']
        con_password = request.POST['conPassword']
        if password != con_password:
            return render(request, 'notes/signup.html', {'error_message': 'Password does not match', 'regForm': regForm})

        try:
            user = User.objects.get(username=username)
            if user is not None:
                regForm = SignUpForm()
                return render(request, 'notes/signup.html', {'regForm': regForm, 'error_message': 'username must be unique'})
        except:
            user = User.objects.create_user(
                username=username, password=password, last_login=timestamp)
            data = {'type': 'user_create',
                    'user_name': user.username, 'user_id': user.id,
                    'timestamp': f'{timestamp}'}
            Emit_event.publish(str(data))
            login(request, user)
            return redirect('index')

    return render(request, 'notes/signup.html', {'error_message': 'Data is not valid', 'regForm': regForm})


def login_view(request):
    # signup 에서 create_user 아니라 create 써서 error나는 거였다.
    username = request.POST['user_id']
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


# get
def index(request):
    notesList = Notes.objects.order_by('-created_at')

    p = Paginator(notesList, 3)
    page_number = request.GET.get('page')

    page_obj = p.get_page(page_number)
    context = {
        'current_user': get_user(request), 'page_obj': page_obj}
    return render(request, 'notes/index.html', context)

# get


def detail(request, note_id):
    try:
        note = Notes.objects.get(pk=note_id)
        color = request.GET.get('color')

    except Notes.DoesNotExist:
        raise Http404("Note does not exist")
    return render(request, 'notes/detail.html', {'notes': note, 'color': color, 'current_user': get_user(request)})

# get


def new(request):
    return render(request, 'notes/new.html')

# post


def create(request):
    # 나중에 삭제 user! user= User.objects.all().get(id=3)

    note = Notes.objects.create(user=get_user(request), title=request.POST.get(
        'note_title'), text=request.POST.get('note_text'))
    timestamp = datetime.now(timezone.utc)
    data = {'type': 'note_create', 'note_id': f'{note.id}', 'note_title': f'{note.title}',
            'note_text': f'{note.text}', 'user_id': '1', 'timestamp': f'{timestamp}'}
    Emit_event.publish(str(data))
    return HttpResponse('<script type="text/javascript">window.close(); window.opener.parent.location.reload();</script>')

# form


def edit(request, note_id):
    note = Notes.objects.get(pk=note_id)
    color = request.GET.get('color')
    return render(request, 'notes/edit.html', {'notes': note, 'color': color})

# put or patch


def update(request, note_id):
    note = Notes.objects.get(pk=note_id)
    # publish data to exchange
    # model_type=data['type'], user_id=data['user_id'],  data=data ['timestamp']
    # later, switch user_id into get_user(request)
    color = request.POST.get('color')
    note.title = request.POST.get("note_title")
    note.text = request.POST.get("note_text")
    update_time = datetime.now(timezone.utc)

    data = {'type': 'note_update', 'note_id': f'{note.id}', 'note_title': f'{note.title}',
            'note_text': f'{note.text}', 'user_id': '1', 'timestamp': f'{update_time}'}
    note.save()
    Emit_event.publish(str(data))
    return HttpResponse('<script type="text/javascript">window.close(); window.opener.parent.location.reload();</script>')

    # return render(request, 'notes/detail.html', {'notes': note, 'color': color})

# delete


def delete(request, note_id):
    try:
        note = Notes.objects.all().get(pk=note_id)
        timestamp = datetime.now(timezone.utc)
        data = {'type': 'note_delete', 'note_id': f'{note.id}', 'note_title': f'{note.title}',
                'note_text': f'{note.text}', 'user_id': '1', 'timestamp': f'{timestamp}'}
        Emit_event.publish(str(data))
        Notes.objects.filter(pk=note_id).delete()

    except Notes.DoesNotExist:
        raise Http404("Note does not exist")
    notesList = Notes.objects.order_by('title')
    return HttpResponse('<script type="text/javascript">window.close(); window.opener.parent.location.reload();</script>')
# post endpoint, and create HttpResponse notes, limit is the number of notes.
# I cannot call request.post/get together in the same endpoint.
# 10000명이 동시에 note create -> 빨리만드려고??????1초안에


def bulk_new(request):
    return render(request, 'notes/new_bulk_create.html')


@ csrf_exempt
def bulk_create(request):
    # data = json.loads(request.body.decode('utf-8')) #this one is when working with postman
    data = request.POST  # this one is with from client request
    for _ in range(int(data['limit'])):
        async_note_create.delay(data)
    return HttpResponse('200')


"""
form -> load balancer -> server request -> ****run code in server (create sql message to the queue)
-> queue -> worker process message -> create sql records

"""
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
