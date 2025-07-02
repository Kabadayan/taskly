from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index_page'),
    path('api/tasks/', views.index_view, name='index'),
    path('create/', views.create_task, name='create_task'),
    path('update/<str:task_id>/', views.update_task, name='update_task'),
    path('delete/<str:task_id>/', views.delete_task, name='delete_task'),
]