# Generated by Django 4.2.11 on 2024-07-08 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0007_remove_milkrecord_employee_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milkrecord',
            name='employee_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portals.employees'),
        ),
    ]