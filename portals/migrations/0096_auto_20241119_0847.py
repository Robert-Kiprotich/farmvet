# Generated by Django 3.1.3 on 2024-11-19 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0095_auto_20241119_0844'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cpdquestions',
            old_name='sections',
            new_name='section',
        ),
    ]
