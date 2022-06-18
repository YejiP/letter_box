from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('<int:note_id>/', views.detail, name='detail'),
    path('<int:note_id>/edit/', views.edit, name='edit'),
    
    path('<int:note_id>/update/', views.update, name='update'),

    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),

    path('<int:note_id>/delete/', views.delete, name='delete'),
    path('signup/', views.signup, name='signup'),
    path('signup_new/', views.signup_new, name='signup_new'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

     # ex: /notes/1/
]