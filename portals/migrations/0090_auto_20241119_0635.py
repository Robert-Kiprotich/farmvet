# Generated by Django 3.1.3 on 2024-11-19 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0089_auto_20241119_0631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cpdquestions',
            name='question_text',
        ),
        migrations.RemoveField(
            model_name='cpdquestions',
            name='tutorial',
        ),
        migrations.RemoveField(
            model_name='cpdquestions',
            name='user',
        ),
    ]
