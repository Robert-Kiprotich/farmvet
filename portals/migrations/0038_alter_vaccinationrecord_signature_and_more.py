# Generated by Django 4.2.11 on 2024-08-22 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0037_alter_vaccinationrecord_signature_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccinationrecord',
            name='signature',
            field=models.ImageField(upload_to='media/signatures/'),
        ),
        migrations.AlterField(
            model_name='vaccinationrecord',
            name='stamp',
            field=models.ImageField(upload_to='media/stamps/'),
        ),
    ]
