# Generated by Django 5.0.6 on 2024-08-08 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_comments_created_at_comments_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='投稿日'),
        ),
    ]
