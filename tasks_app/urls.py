from django.urls import path
from . import views

app_name = 'tasks_app'

urlpatterns = [
    path('test/', views.test_view, name='test'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/delete/', views.delete_task, name='delete_task'),
    path('labels/create/', views.create_label, name='create_label'),
    path('labels/delete/', views.delete_label, name='delete_label'),
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
] 