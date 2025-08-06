from rest_framework import serializers
from .models import Task, Tag, Category, Note, CustomUser


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


class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Task
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'content']
        read_only_fields = ['task']

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance