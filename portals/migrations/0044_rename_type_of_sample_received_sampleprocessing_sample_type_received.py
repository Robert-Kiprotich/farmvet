# Generated by Django 4.2.11 on 2024-08-29 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0043_alter_laboratoryrecord_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sampleprocessing',
            old_name='type_of_sample_received',
            new_name='sample_type_received',
        ),
    ]
