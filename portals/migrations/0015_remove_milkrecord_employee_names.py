# Generated by Django 4.2.11 on 2024-07-08 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0014_alter_milkrecord_employee_names'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='milkrecord',
            name='employee_names',
        ),
    ]
