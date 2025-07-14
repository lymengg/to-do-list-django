from rest_framework import serializers
from .models import Task, Tag, Category

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

class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    class Meta:
        model = Task
        fields = '__all__'