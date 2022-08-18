import pwd
from django.shortcuts import render
from django.shortcuts import redirect
from .tasks import async_note_create
from .models import Notes
from .models import Friend_request
from .models import Friendship

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
    try:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    except:
        pass
    context = {
        'current_user': get_user(request), 'page_obj': None, 'friends': None, 'outbox': False, 'loginFailed': True}
    return render(request, 'notes/index.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')


# get
def index(request):
    if get_user(request).username:
        outbox = False

        try:
            if request.GET['mailbox'] == 'outbox':
                outbox = True
                notesList = Notes.objects.filter(
                    sender=get_user(request)).order_by('-created_at')
        except:
            outbox = False
            notesList = Notes.objects.filter(
                receiver=get_user(request)).order_by('-created_at')

        p = Paginator(notesList, 3)
        page_number = request.GET.get('page')
        friends = Friendship.objects.filter(me=get_user(request))

        page_obj = p.get_page(page_number)
        context = {
            'current_user': get_user(request), 'page_obj': page_obj, 'friends': friends, 'outbox': outbox, 'loginFailed': False}
    else:
        context = {
            'current_user': get_user(request), 'page_obj': None, 'friends': None, 'outbox': False, 'loginFailed': False}
    return render(request, 'notes/index.html', context)

# get


def detail(request, note_id):
    try:
        note = Notes.objects.get(pk=note_id)
        color = request.GET.get('color')
        if request.GET.get('outbox') == "False":
            note.read = True
            note.save()

    except Notes.DoesNotExist:
        raise Http404("Note does not exist")
    return render(request, 'notes/detail.html', {'notes': note, 'color': color, 'current_user': get_user(request)})

# get


def new(request):
    data = {'receiver': None}
    if request.GET['receiver']:
        data['receiver'] = request.GET['receiver']
    return render(request, 'notes/new.html', data)

# post


def create(request):
    note = Notes.objects.create(sender=get_user(request), receiver=User.objects.get(username=request.POST.get('receiver')), title=request.POST.get(
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


def accept_friend(request):
    with_whom = User.objects.get(username=request.GET['with'])
    Friend_request.objects.filter(
        from_user=with_whom).filter(to_user=get_user(request)).delete()
    Friendship.objects.create(me=with_whom, my_friend=get_user(request))
    if not Friendship.objects.filter(me=get_user(request)).filter(my_friend=with_whom):
        Friendship.objects.create(me=get_user(request), my_friend=with_whom)
    return redirect('add_friend')


def add_friend(request):
    # construct data dictionary
    data = {'pending_request': [], 'my_request': [],
            'friends': [], 'friend_username': None, 'already_friend': False, 'received': False, 'pending': False, 'noID': False}
    data['pending_request'] = Friend_request.objects.filter(
        from_user=get_user(request))
    data['my_request'] = Friend_request.objects.filter(
        to_user=get_user(request))
    data['friends'] = Friendship.objects.filter(me=get_user(request))

    # process request according to request method
    if request.method == 'GET':
        return render(request, 'notes/add_friend.html', data)

    elif request.method == 'POST':
        try:
            friend = User.objects.get(username=request.POST['friend_username'])
            if friend:
                data['noID'] = False
                data['friend_username'] = friend.username
                # see if i already add this person to my friend
                if Friendship.objects.filter(my_friend__username=request.POST['friend_username']).filter(me=get_user(request)):
                    data['already_friend'] = True
                elif Friend_request.objects.filter(to_user=get_user(request)).filter(from_user__username=request.POST['friend_username']):
                    data['received'] = True
                elif Friend_request.objects.filter(from_user=get_user(request)).filter(to_user__username=request.POST['friend_username']):
                    data['pending'] = True
        except:
            data['noID'] = True

        return render(request, 'notes/add_friend.html', data)


def send_friend_request(request):
    if request.method == 'GET':
        to_user = User.objects.get(username=request.GET['friend_username'])
        if not Friend_request.objects.filter(from_user=get_user(request)).filter(to_user=to_user):
            Friend_request.objects.create(
                from_user=get_user(request), to_user=to_user)
            return redirect('add_friend')
        else:
            return HttpResponse('<script type="text/javascript">alert("already added");window.location.href="/notes/add_friend/"</script>')
