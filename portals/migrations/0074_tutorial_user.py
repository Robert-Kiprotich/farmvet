# Generated by Django 4.2.11 on 2024-11-06 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portals', '0073_rename_title_tutorial_lesson_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorial',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
