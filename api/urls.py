from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='api_home'),
    path('tasks/', views.TaskListApiView.as_view(), name='tasks'),
    path('tasks/create', views.TaskCreateApiView.as_view(), name='task_create'),
    path('tasks/<int:pk>', views.TaskDetailApiView.as_view(), name='task_detail'),
    path('tasks/update/<int:pk>', views.TaskUpdateApiView.as_view(), name='task_update'),
    path('tasks/delete/<int:pk>', views.TaskDeleteApiView.as_view(), name='task_delete'),
]