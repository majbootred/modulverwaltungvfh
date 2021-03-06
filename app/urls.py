from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('assignment-new', views.assignment_new_view, name='assignment-new'),
    path('assignment-edit/<int:pk>', views.assignment_edit_view, name='assignment-edit'),
    path('assignment-delete/<int:pk>', views.assignment_delete_view, name='assignment-delete'),
    path('ajax/get_modules', views.get_modules_view, name='get_modules'),
]