# Generated by Django 4.2.11 on 2024-08-28 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0038_alter_vaccinationrecord_signature_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccinationrecord',
            name='signature',
            field=models.ImageField(upload_to='signatures/'),
        ),
        migrations.AlterField(
            model_name='vaccinationrecord',
            name='stamp',
            field=models.ImageField(upload_to='stamps/'),
        ),
    ]