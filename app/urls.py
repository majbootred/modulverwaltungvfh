from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('assignment-new', views.assignment_new_view, name='assignment'),
    path('assignment-edit/<int:pk>', views.assignment_edit_view, name='assignment'),

    #nur Testansichten - vor Abgabe rausnehmen
    path('modulelist', views.modulelist_view, name='modulelist'),
    path('prereqlist/<modul>', views.prereqlist_view, name='prereqlist'),
]