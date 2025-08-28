from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hex_color = models.CharField(max_length=50, null=True)  # Default to white

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "tag"

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS = [
        ('INIT', 'Init'),
        ('IN_PROGRESS', 'In Progress'),
        ('CANCEL', 'Cancel'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # One-to-Many (each Task belongs to one Category)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="tasks")

    # Many-to-Many (each Task can have multiple Tags)
    tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")

    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default='INIT')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "task"

    def __str__(self):
        return self.title


class Note(models.Model):
    content = models.TextField(max_length=500)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.content


class UserProfile(models.Model):
    # Composition: keep a one-to-one relation with the built-in User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # Extra fields
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "user_profile"

    def __str__(self):
        return f"{self.user.username}'s Profile"
