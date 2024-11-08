# Generated by Django 4.2.11 on 2024-08-22 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0035_remove_postmortemrecord_signature_and_stamp_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='laboratoryrecord',
            old_name='vet_signature',
            new_name='signature',
        ),
        migrations.RenameField(
            model_name='laboratoryrecord',
            old_name='stamp_line',
            new_name='stamp',
        ),
        migrations.RenameField(
            model_name='samplecollection',
            old_name='stamp_line',
            new_name='stamp',
        ),
        migrations.RenameField(
            model_name='surgicalrecord',
            old_name='stamp_line',
            new_name='stamp',
        ),
        migrations.RenameField(
            model_name='vaccinationrecord',
            old_name='stamp_line',
            new_name='stamp',
        ),
        migrations.RemoveField(
            model_name='sampleprocessing',
            name='stamp_line',
        ),
        migrations.RemoveField(
            model_name='sampleprocessing',
            name='vet_signature',
        ),
        migrations.AddField(
            model_name='sampleprocessing',
            name='signature',
            field=models.ImageField(default='dhsfgey', upload_to='signatures/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sampleprocessing',
            name='stamp',
            field=models.ImageField(default='dsfeer', upload_to='stamps/'),
            preserve_default=False,
        ),
    ]
