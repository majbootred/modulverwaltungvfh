from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('modulelist', views.modulelist, name='modulelist'),
    path('prereqlist/<modul>', views.prereqlist, name='prereqlist'),
]