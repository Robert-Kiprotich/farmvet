# Generated by Django 4.2.11 on 2024-08-29 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0044_rename_type_of_sample_received_sampleprocessing_sample_type_received'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sampleprocessing',
            old_name='name_of_animal',
            new_name='animal_name',
        ),
    ]
