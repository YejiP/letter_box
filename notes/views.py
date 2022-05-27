from django.shortcuts import render
from django.http import HttpResponse
from .models import Notes
from django.http import Http404

"""
index : display notes by time
detail : retreive the note object, then edit
Now in your time on the web you may have come across such beauties as ME2/Sites/dirmod.htm?sid=&type=gen&mod=Core+Pages&gid=A6CD4967199A42D9B65B1B. You will be pleased to know that Django allows us much more elegant URL patterns than that.
To get from a URL to a view, Django uses what are known as ‘URLconfs’. A URLconf maps URL patterns to views.


"""
def index(request):
    notesList = Notes.objects.order_by('title')
    context = {'latest_Note_list': notesList}
    return render(request, 'notes/index.html', context)


def detail(request, note_id):
    try:
        note = Notes.objects.get(pk=note_id)
    except Notes.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'notes/detail.html', {'notes': note})