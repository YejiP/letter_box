from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('<int:note_id>/', views.detail, name='detail'),
    path('<int:note_id>/edit/', views.edit, name='edit'),
    
    path('<int:note_id>/update/', views.update, name='update'),

    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),

    path('bulk_create/', views.bulk_create, name='bulk_create'),

    path('<int:note_id>/delete/', views.delete, name='delete'),
    path('signup/', views.signup, name='signup'),
    path('signup_new/', views.signup_new, name='signup_new'),

    path('login_view/', views.login_view, name='login_view'),
    path('logout_view/', views.logout_view, name='logout_view'),

     # ex: /notes/1/
    #이렇게하면 리소스로 헷갈릴수있어서 절대일케하면안된다.
     # notes/bulk_create/3/ => notes/bulk_create?limit=3
]