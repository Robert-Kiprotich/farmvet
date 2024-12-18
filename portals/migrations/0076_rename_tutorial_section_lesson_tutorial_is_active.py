# Generated by Django 4.2.11 on 2024-11-07 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0075_tutorial_unit_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section',
            old_name='tutorial',
            new_name='lesson',
        ),
        migrations.AddField(
            model_name='tutorial',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
