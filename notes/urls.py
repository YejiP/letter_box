from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
     # ex: /notes/1/
    path('<int:note_id>/', views.detail, name='detail'),
]