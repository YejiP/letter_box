from django.urls import path

from . import note_views
from . import user_views

urlpatterns = [
    path('', note_views.index, name='index'),

    path('<int:note_id>/', note_views.detail, name='detail'),
    path('<int:note_id>/edit/', note_views.edit, name='edit'),

    path('<int:note_id>/update/', note_views.update, name='update'),

    path('new/', note_views.new, name='new'),
    path('create/', note_views.create, name='create'),
    path('<int:note_id>/delete/', note_views.delete, name='delete'),


    path('signup/', user_views.signup, name='signup'),
    path('signup_new/', user_views.signup_new, name='signup_new'),

    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),

    path('add_friend/', user_views.add_friend, name='add_friend'),
    path('send_friend_reqeust/', user_views.send_friend_request,
         name='send_friend_request'),
    path('accept_friend/', user_views.accept_friend, name='accept_friend'),
    path('friend_info/', user_views.friend_info, name='friend_info')

]
