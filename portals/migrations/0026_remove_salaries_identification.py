# Generated by Django 4.2.11 on 2024-08-10 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0025_veterinarydrugs_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salaries',
            name='identification',
        ),
    ]
