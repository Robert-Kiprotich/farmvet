# Generated by Django 4.2.11 on 2024-09-26 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0054_alter_artificialinsemination_insemination_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artificialinsemination',
            name='vet_reg_no',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
