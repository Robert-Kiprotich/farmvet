# Generated by Django 3.1.3 on 2024-12-29 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0131_remove_dailykill_livestock_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailykill',
            name='livestock_category',
            field=models.CharField(choices=[('Cattle', 'Cattle'), ('Sheep', 'Sheep'), ('Goat', 'Goat'), ('Pig', 'Pig')], default='Sheep', max_length=50),
            preserve_default=False,
        ),
    ]