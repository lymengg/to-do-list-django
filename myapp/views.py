from rest_framework.viewsets import ModelViewSet
from .models import Tag, Category
from .models import Task
from .serializer import CategorySerializer, TagSerializer, TaskSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
