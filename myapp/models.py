from django.db import models


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

    def str(self):
        return self.title