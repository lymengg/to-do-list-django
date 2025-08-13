from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hex_color = models.CharField(max_length=50, null=True)  # Default to white

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

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

    def __str__(self):
        return self.title


class Note(models.Model):
    content = models.TextField(max_length=500)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.content

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, address, first_name=None, last_name=None, password=None, **extra_fields):
        if not username or username.strip() == '':
            raise ValueError('The Username field is required and cannot be empty.')
        if not email or email.strip() == '':
            raise ValueError('The Email field is required and cannot be empty.')
        if not address or address.strip() == '':
            raise ValueError('The Address field is required and cannot be empty.')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            address=address,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, address, first_name=None, last_name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, address, first_name, last_name, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, blank=False)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=False)  # Make required here

    REQUIRED_FIELDS = ['email', 'address']

    objects = CustomUserManager()
