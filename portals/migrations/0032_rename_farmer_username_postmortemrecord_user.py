# Generated by Django 4.2.11 on 2024-08-22 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0031_remove_surgicalrecord_farmer_username_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postmortemrecord',
            old_name='farmer_username',
            new_name='user',
        ),
    ]
