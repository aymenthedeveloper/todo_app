from rest_framework import generics
from main.models import Task
from api.serializers import TaskSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from django.contrib.sites.shortcuts import get_current_site
from .permissions import IsOwnerPermission


@api_view(['GET'])
def home(request):
    site = get_current_site(request).domain
    data = {
        "api overview": f"http://{site}/api/",
        "list all tasks": f"http://{site}/api/tasks/",
        "task details": f"http://{site}/api/tasks/<int:pk>",
        "create task": f"http://{site}/api/tasks/create/",
        "update task": f"http://{site}/api/tasks/update/<int:pk>",
        "delete task": f"http://{site}/api/tasks/delete/<int:pk>",
    }
    return Response(data)


class TaskListApiView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class TaskCreateApiView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class TaskDetailApiView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]
    lookup_field = 'pk'

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(user=self.request.user)


class TaskUpdateApiView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)



class TaskDeleteApiView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


