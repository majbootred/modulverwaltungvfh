from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('modulelist', views.modulelist, name='modulelist'),
    path('prereqlist/<modul>', views.prereqlist, name='prereqlist'),
]