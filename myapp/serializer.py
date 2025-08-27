from django.contrib.auth.models import BaseUserManager
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

class CustomUserSerializer(serializers.ModelSerializer):
    # Explicitly declare so DRF doesn't inherit model's optional behavior
    username = serializers.CharField(required=True)  # we'll enforce in validate()
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'address', 'password'
        ]

    def validate(self, data):
        """Custom required fields logic."""
        if self.instance is None:  # Create mode
            missing_fields = []
            for field in ['username', 'email', 'password']:
                if not data.get(field):
                    missing_fields.append(field)
            if missing_fields:
                raise serializers.ValidationError({
                    f: "This field is required." for f in missing_fields
                })
        return data

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