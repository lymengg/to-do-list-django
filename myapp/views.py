from rest_framework import permissions
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet
from .models import Tag, Category, Task, Note, CustomUser
from .serializer import CategorySerializer, TagSerializer, TaskSerializer, NoteSerializer, CustomUserSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()   # <-- Add this line
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer

    def get_queryset(self):
        task_id = self.kwargs.get('task_pk')
        return Note.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_pk')
        task = Task.objects.get(pk=task_id)  # This raises DoesNotExist if not found
        serializer.save(task=task)

class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer