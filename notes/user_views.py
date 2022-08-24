from operator import truediv
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Notes, User
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user, logout
from .form import SignUpForm
from .models import Friendship
from django.db.models import Q
from datetime import datetime, timezone
from django.http import JsonResponse


def signup_new(request):
    regForm = SignUpForm()
    return render(request, 'signup.html', {'regForm': regForm})


def signup(request):
    regForm = SignUpForm(request.POST)
    if regForm.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        con_password = request.POST['conPassword']
        if password != con_password:
            return render(request, 'signup.html', {'regForm': regForm, 'error_message': 'Password does not match'})
        try:
            user = User.objects.get(username=username)
            if user is not None:
                return render(request, 'signup.html', {'regForm': regForm, 'error_message': 'username must be unique'})
        except:
            timestamp = datetime.now(timezone.utc)
            user = User.objects.create_user(
                username=username, password=password, last_login=timestamp
            )
            login(request, user)
            callie = User.objects.get(username='callie')
            Friendship.objects.create(
                user=get_user(request), friend=callie, status=True)
            Notes.objects.create(sender=callie,
                                 receiver=get_user(request),
                                 title='Welcome to Stickies!',
                                 text='Express whatever.. to your friends! =)')
        return redirect('index')
    return render(request, 'signup.html', {'regForm': regForm, 'error_message': 'Data is not valid'})


def login_view(request):
    username = request.POST['user_id']
    password = request.POST['user_pwd']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('index')

    request.session['loginFailed'] = True
    return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('index')


def add_friend(request):
    data = {
        'pending_request': Friendship.objects.filter(
            Q(user=get_user(request)) & Q(status=False)),
        'my_request':  Friendship.objects.filter(
            Q(friend=get_user(request)) & Q(status=False)),
        'friends': Friendship.objects.filter(
            Q(user=get_user(request)) | Q(friend=get_user(request)) & Q(status=True)),
        'friend_username': None,
        'myself': False,
        'already_friend': False,
        'received': False,
        'pending': False,
        'noID': False
    }

    # process request according to request method
    if request.method == 'GET':
        return render(request, 'add_friend.html', data)

    elif request.method == 'POST':
        try:
            if request.POST['friend_username'] == get_user(request).username:
                data['myself'] = True
                return render(request, 'add_friend.html', data)

            friend = User.objects.get(username=request.POST['friend_username'])
            if friend:
                data['noID'] = False
                data['friend_username'] = friend.username
                # see if i already add this person to my friend
                fa = Friendship.objects.filter(
                    user__username=friend.username).filter(friend__username=get_user(request).username)
                fb = Friendship.objects.filter(
                    friend__username=friend.username).filter(user__username=get_user(request).username)

                if fa.filter(status=True) or fb.filter(status=True):
                    data['already_friend'] = True
                elif fa:
                    data['received'] = True
                elif fb:
                    data['pending'] = True
        except:
            data['noID'] = True

        return render(request, 'add_friend.html', data)

# this function will be hit if friend exist, but not pending.


def send_friend_request(request):
    to_user = User.objects.get(username=request.GET['friend_username'])
    Friendship.objects.create(
        user=get_user(request), friend=to_user, status=False)
    return redirect('add_friend')


def accept_friend(request):
    with_whom = User.objects.get(username=request.GET['with'])
    friend = Friendship.objects.filter(
        user=with_whom).get(friend=get_user(request))
    friend.status = True
    friend.save()
    return redirect('add_friend')


def friend_info(request):
    if request.method == "GET":
        friends_obj = Friendship.objects.filter(Q(
            user=get_user(request)) & Q(status=True))
        friends_obj2 = Friendship.objects.filter(Q(
            friend=get_user(request)) & Q(status=True))
        friends = list(map(lambda x: x.friend.username, friends_obj)) +\
            list(map(lambda x: x.user.username, friends_obj2))
        friends.sort()
        new_request = Friendship.objects.filter(
            Q(friend__username=get_user(request)) & Q(status=False)).count()
        print(new_request)
        return JsonResponse({'friend': friends, 'new_request': new_request}, status=200)
    return JsonResponse({}, status=400)
