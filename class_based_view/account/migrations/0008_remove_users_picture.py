# Generated by Django 5.0.6 on 2024-08-09 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_remove_comments_create_at_remove_comments_update_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='picture',
        ),
    ]
