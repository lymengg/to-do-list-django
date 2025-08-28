from django.contrib.auth.models import BaseUserManager
from rest_framework import serializers
from .models import Task, Tag, Category, Note

class CategorySerializer(serializers.ModelSerializer):
    task_count = serializers.IntegerField(source='tasks.count', read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'hex_color', 'task_count', 'status']

    def get_task_count(self, obj):
        return obj.tasks.count()

    def get_status(self, obj):
        count = obj.tasks.count()
        if count == 0:
            return "None"
        elif count < 3:
            return "A few"
        else:
            return "Too Many"


class TagSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    task_count = serializers.IntegerField(source='tasks.count', read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['name', 'task_count', 'status']

    def get_task_count(self, obj):
        return obj.tasks.count()

    def get_status(self, obj):
        count = obj.tasks.count()
        if count == 0:
            return "None"
        elif count < 3:
            return "A few"
        else:
            return "Too Many"

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)  # nested notes
    tags = serializers.StringRelatedField(many=True, read_only=True)  # or use TagSerializer

    class Meta:
        model = Task
        fields = "__all__"