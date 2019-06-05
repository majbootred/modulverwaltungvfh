from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    #nur Testansichten - vor Abgabe rausnehmen
    path('modulelist', views.modulelist, name='modulelist'),
    path('prereqlist/<modul>', views.prereqlist, name='prereqlist'),
]