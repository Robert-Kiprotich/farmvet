# Generated by Django 3.1.3 on 2024-11-19 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0084_auto_20241119_0615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cpdquestions',
            name='tutorial',
        ),
    ]
