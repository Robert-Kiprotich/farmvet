# Generated by Django 3.1.3 on 2024-11-29 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0105_auto_20241129_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessmentrecord',
            name='signature_and_stamp',
            field=models.CharField(max_length=100),
        ),
    ]