# Generated by Django 3.1.3 on 2024-11-19 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0094_auto_20241119_0803'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cpdquestions',
            old_name='section',
            new_name='sections',
        ),
    ]