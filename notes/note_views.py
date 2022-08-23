from django.shortcuts import render

from notes.user_views import friend_info
from .models import Notes
from .models import Friendship
from django.db.models import Q
from .models import User
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.core.paginator import Paginator
import json


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

        context = {
            'current_user': get_user(request),
            'page_obj': page_obj,
            'outbox': outbox,
            'friends': json.loads(friend_info(request).content.decode('utf-8'))["friend"],
            'new_request': json.loads(friend_info(request).content.decode('utf-8'))["new_request"],
            'loginFailed': False
        }
    return render(request, 'index.html', context)


def new(request):
    return render(request, 'new.html', {'receiver': request.GET['receiver']})


def detail(request, note_id):
    try:
        note = Notes.objects.get(pk=note_id)

        if note.receiver != get_user(request) and note.sender != get_user(request):
            return render(request, 'error.html', {'error_message': 'You are not authorized to see this note.'})

        color = request.GET.get('color')

        if request.GET.get('mailbox') == "inbox":
            note.read = True
            note.save()

    except:
        return render(request, 'error.html', {'error_message': 'Resource does not exist.'})

    return render(request, 'detail.html', {'notes': note, 'color': color, 'current_user': get_user(request)})


def create(request):
    try:
        sender = get_user(request)
        receiver = User.objects.get(
            username=request.POST.get('receiver'))

        Notes.objects.create(sender=sender,
                             receiver=receiver,
                             title=request.POST.get('note_title'),
                             text=request.POST.get('note_text'))
    except:
        return render(request, 'error.html')

    return render(request, 'close.html')


def edit(request, note_id):
    try:
        note = Notes.objects.get(pk=note_id)
        if note.receiver != get_user(request) and note.sender != get_user(request):
            return render(request, 'error.html', {'error_message': 'You are not authorized to see this note.'})
        color = request.GET.get('color')

    except:
        return render(request, 'error.html', {'error_message': 'Resource does not exist.'})

    return render(request, 'edit.html', {'notes': note, 'color': color})

# put or patch


def update(request, note_id):
    try:
        note = Notes.objects.get(pk=note_id)
        if note.receiver != get_user(request) and note.sender != get_user(request):
            return render(request, 'error.html', {'error_message': 'You are not authorized to see this note.'})

        note.title = request.POST.get("note_title")
        note.text = request.POST.get("note_text")
        note.save()
    except:
        return render(request, 'error.html', {'error_message': 'Resource does not exist.'})

    return render(request, 'close.html')


def delete(request, note_id):
    try:
        note = Notes.objects.all().get(pk=note_id)
        if note.receiver != get_user(request) and note.sender != get_user(request):
            return render(request, 'error.html', {'error_message': 'You are not authorized to see this note.'})

        Notes.objects.filter(pk=note_id).delete()
    except:
        return render(request, 'error.html', {'error_message': 'Resource does not exist.'})

    return render(request, 'close.html')
