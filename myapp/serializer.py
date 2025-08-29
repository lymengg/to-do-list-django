from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from .models import Task, Tag, Category, Note, UserProfile


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


User = get_user_model()


# Response serializer
class UserSerializer(BaseUserSerializer):
    birthdate = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "birthdate")

    def get_birthdate(self, obj):
        if hasattr(obj, "profile"):
            return obj.profile.birthdate
        return None


# Serializer for creating user
class UserCreateSerializer(BaseUserCreateSerializer):
    re_password = serializers.CharField(write_only=True)
    birthdate = serializers.DateField(required=True, write_only=True)  # 👈 add write_only

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ("id", "username", "password", "re_password",
                  "email", "first_name", "last_name", "birthdate")

    def validate(self, data):
        if data["password"] != data["re_password"]:
            raise serializers.ValidationError({"re_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        birthdate = validated_data.pop("birthdate", None)
        validated_data.pop("re_password", None)

        user = super().create(validated_data)

        # create profile and save birthdate
        profile, _ = UserProfile.objects.get_or_create(user=user)
        if birthdate:
            profile.birthdate = birthdate
            profile.save()

        return user

    def to_representation(self, instance):
        # Use the same representation as UserSerializer
        return UserSerializer(instance, context=self.context).data
