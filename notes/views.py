import pwd
from django.shortcuts import render
from django.shortcuts import redirect
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
from .event_publisher import EventPublisher
from datetime import datetime, timezone
from django.core.paginator import Paginator
from .form import SignUpForm

# ?? folder??
# user/notes view should be in a separate file


def signup_new(request):
    regForm = SignUpForm()
    return render(request, 'notes/signup.html', {'regForm': regForm})


def signup(request):
    # if request.method == 'POST':
    regForm = SignUpForm(request.POST)  # form needs content
    if regForm.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        con_password = request.POST['conPassword']
        if password != con_password:
            return render(request, 'notes/signup.html', {'regForm': regForm, 'error_message': 'Password does not match'})
        try:
            user = User.objects.get(username=username)
            if user is not None:
                return render(request, 'notes/signup.html', {'regForm': regForm, 'error_message': 'username must be unique'})
        except:
            timestamp = datetime.now(timezone.utc)
            user = User.objects.create_user(
                username=username, password=password, last_login=timestamp
            )
            data = {
                'type': 'user_create',
                'username': user.username,
                'user_id': user.id,
                'timestamp': f'{timestamp}'
            }
            EventPublisher.publish(str(data))
            login(request, user)
            return redirect('index')

    return render(request, 'notes/signup.html', {'regForm': regForm, 'error_message': 'Data is not valid'})


def login_view(request):
    # signup 에서 create_user 아니라 create 써서 error나는 거였다.
    username = request.POST['user_id']
    password = request.POST['user_pwd']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('index')

    context = {
        'current_user': get_user(request),
        'page_obj': None,
        'friends': None,
        'outbox': False,
        'loginFailed': True
    }
    return render(request, 'notes/index.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')


def index(request):
    context = {}
    if get_user(request).username:
        outbox = False
        if 'mailbox' in request.GET and request.GET['mailbox'] == 'outbox':
            outbox = True
            notesList = Notes.objects.filter(
                sender=get_user(request)).order_by('-created_at')
        else:
            outbox = False
            notesList = Notes.objects.filter(
                receiver=get_user(request)).order_by('-created_at')

        p = Paginator(notesList, 3)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)

        friends = Friendship.objects.filter(me=get_user(request))

        context = {
            'current_user': get_user(request),
            'page_obj': page_obj,
            'friends': friends,
            'outbox': outbox,
            'loginFailed': False
        }
    return render(request, 'notes/index.html', context)

# get

# if user does not match, they should not be able to see!!!!! authrization


def detail(request, note_id):
    note = Notes.objects.get(pk=note_id)
    color = request.GET.get('color')
    # check the boolean not string
    if request.GET.get('outbox') == "False":
        note.read = True
        note.save()
    return render(request, 'notes/detail.html', {'notes': note, 'color': color, 'current_user': get_user(request)})

# get


def new(request):
    return render(request, 'notes/new.html', {'receiver': request.GET['receiver']})

# post


def create(request):
    sender = get_user(request)
    receiver = User.objects.get(
        username=request.POST.get('receiver'))

    note = Notes.objects.create(sender=sender,
                                receiver=receiver,
                                title=request.POST.get('note_title'),
                                text=request.POST.get('note_text'))

    # model.models,에서.. add this audit.. when create method is called
    timestamp = datetime.now(timezone.utc)
    data = {
        'type': 'note_create',
        'note_id': f'{note.id}',
        'note_title': f'{note.title}',
        'note_text': f'{note.text}',
        'user_id': sender,
        'timestamp': f'{timestamp}'
    }
    EventPublisher.publish(str(data))

    # this is wrong.. find sth else
    return HttpResponse('<script type="text/javascript">window.close(); window.opener.parent.location.reload();</script>')

# form


def edit(request, note_id):
    note = Notes.objects.get(pk=note_id)
    color = request.GET.get('color')
    return render(request, 'notes/edit.html', {'notes': note, 'color': color})

# put or patch


def update(request, note_id):
    note = Notes.objects.get(pk=note_id)
    note.title = request.POST.get("note_title")
    note.text = request.POST.get("note_text")
    note.save()

    data = {
        'type': 'note_update',
        'note_id': f'{note.id}',
        'note_title': f'{note.title}',
        'note_text': f'{note.text}',
        'user_id': get_user(request),
        'timestamp': f'{datetime.now(timezone.utc)}'
    }
    EventPublisher.publish(str(data))
    # fix this -> API should not control UI!!!!!!!!!!!!!! practice encapsulatoin
    return HttpResponse('<script type="text/javascript">window.close(); window.opener.parent.location.reload();</script>')


# delete


def delete(request, note_id):
    note = Notes.objects.all().get(pk=note_id)
    Notes.objects.filter(pk=note_id).delete()
    # this
    return HttpResponse('<script type="text/javascript">window.close(); window.opener.parent.location.reload();</script>')


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
    data = {
        'pending_request': [],
        'my_request': [],
        'friends': [],
        'friend_username': None,
        'already_friend': False,
        'received': False,
        'pending': False,
        'noID': False
    }
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
