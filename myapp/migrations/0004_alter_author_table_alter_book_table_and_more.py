# Generated by Django 5.2 on 2025-05-23 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_author_genre_book_publication_date_alter_book_author_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='author',
            table='author',
        ),
        migrations.AlterModelTable(
            name='book',
            table='book',
        ),
        migrations.AlterModelTable(
            name='genre',
            table='genre',
        ),
        migrations.AlterModelTable(
            name='profile',
            table='profile',
        ),
    ]
