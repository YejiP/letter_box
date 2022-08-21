from django.shortcuts import render
from django.shortcuts import redirect
from .models import Notes
from .models import Friendship
from django.db.models import Q

from .models import User
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import get_user, logout
from django.utils import timezone
from .event_publisher import EventPublisher
from datetime import datetime, timezone
from django.core.paginator import Paginator

# user/notes view should be in a separate file


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

        friends_obj = Friendship.objects.filter(Q(
            user=get_user(request)) & Q(status=True))
        friends_obj2 = Friendship.objects.filter(Q(
            friend=get_user(request)) & Q(status=True))
        friends = list(map(lambda x: x.friend.username, friends_obj)) + \
            list(map(lambda x: x.user.username, friends_obj2))
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
    print(request.GET)
    if request.GET.get('mailbox') == "inbox":
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
