from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index_view, name='index'),
    #nur Testansichten - vor Abgabe rausnehmen
    path('modulelist', views.modulelist_view, name='modulelist'),
    path('prereqlist/<modul>', views.prereqlist_view, name='prereqlist'),
]