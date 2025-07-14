from django.core.management.base import BaseCommand
from faker import Faker
import random
from myapp.models import Task, Category, Tag

class Command(BaseCommand):
    help = "Seed database with dummy data"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Categories
        for _ in range(5):
            Category.objects.get_or_create(name=fake.word().capitalize())

        # Create Tags
        for _ in range(10):
            Tag.objects.get_or_create(name=fake.word())

        categories = list(Category.objects.all())
        tags = list(Tag.objects.all())

        # Create Tasks
        for _ in range(20):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.text(),
                category=random.choice(categories),
                is_completed=fake.boolean(),
                due_date=fake.date_this_year()
            )
            task.tags.set(random.sample(tags, k=random.randint(1, 3)))

        self.stdout.write(self.style.SUCCESS("✅ Dummy data created!"))
