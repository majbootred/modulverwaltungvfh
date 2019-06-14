from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('assignment-new', views.assignment_new_view, name='assignment_new'),
    path('assignment-edit/<int:pk>', views.assignment_edit_view, name='assignment_edit'),
    path('assignment-delete/<int:pk>', views.assignment_delete_view, name='assignment-delete'),
    path('ajax/get_modules', views.get_modules_view, name='get_modules'),
    #nur Testansichten - vor Abgabe rausnehmen
    path('modulelist', views.modulelist_view, name='modulelist'),
    path('prerequisites/<my_module>', views.prerequisites_view, name='prerequisites'),

]