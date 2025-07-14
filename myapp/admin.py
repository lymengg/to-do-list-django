from django.contrib import admin
from .models import Task, Category, Tag


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'sort_desc',
                    'status', 'category', 'tags_list']
    list_editable = ['status']
    list_per_page = 5
    search_fields = ['title']

    def sort_desc(self, task: Task):
        words = task.description.split()
        return " ".join(words[:4]) + "..."
        #  return task.description

    sort_desc.short_description = 'Desc'

    def tags_list(self, task: Task):
        all_tags_in_task = task.tags.all()
        list_tags = []
        for tag in all_tags_in_task:
            list_tags.append(tag.name)
            return list_tags

    tags_list.short_description = 'Tags'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
    list_display = ['name', 'hex_color', 'task_count']
    search_fields = ['name']

    def task_count(self, category: Category):
        return category.tasks.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'task_count']  # Show name and task count in admin

    def task_count(self, tag: Tag):
        return tag.tasks.count()

    task_count.short_description = 'Count'
