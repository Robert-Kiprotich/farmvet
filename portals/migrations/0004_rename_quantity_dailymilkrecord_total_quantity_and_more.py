# Generated by Django 4.2.11 on 2024-07-05 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0003_rename_total_quantity_weeklymilkrecord_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dailymilkrecord',
            old_name='quantity',
            new_name='total_quantity',
        ),
        migrations.RenameField(
            model_name='weeklymilkrecord',
            old_name='quantity',
            new_name='total_quantity',
        ),
    ]
