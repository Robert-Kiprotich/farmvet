# Generated by Django 3.1.3 on 2024-12-30 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0135_auto_20241230_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='noobjection',
            name='county',
            field=models.CharField(default='kericho', max_length=100),
            preserve_default=False,
        ),
    ]
