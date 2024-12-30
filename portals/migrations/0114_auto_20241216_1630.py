# Generated by Django 3.1.3 on 2024-12-16 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0113_practitioner'),
    ]

    operations = [
        migrations.AddField(
            model_name='artificialinsemination',
            name='sub_county',
            field=models.CharField(default='kericho', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artificialinsemination',
            name='ward',
            field=models.CharField(default='weem', max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='practitioner',
            name='area_of_operation',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='practitioner',
            name='county',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='practitioner',
            name='first_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='practitioner',
            name='last_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='practitioner',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='practitioner',
            name='registration_number',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='practitioner',
            name='specialization',
            field=models.CharField(choices=[('large_animals', 'Large Animals'), ('small_animals', 'Small Animals')], max_length=50),
        ),
        migrations.AlterField(
            model_name='practitioner',
            name='subcounty',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='practitioner',
            name='vet_category',
            field=models.CharField(choices=[('surgeon', 'Surgeon'), ('technologist', 'Technologist'), ('technician', 'Technician')], max_length=50),
        ),
        migrations.AlterField(
            model_name='practitioner',
            name='ward',
            field=models.CharField(max_length=30),
        ),
    ]