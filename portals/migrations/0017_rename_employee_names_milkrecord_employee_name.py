# Generated by Django 4.2.11 on 2024-07-08 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0016_milkrecord_employee_names'),
    ]

    operations = [
        migrations.RenameField(
            model_name='milkrecord',
            old_name='employee_names',
            new_name='employee_name',
        ),
    ]
