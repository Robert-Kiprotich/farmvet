# Generated by Django 4.2.11 on 2024-07-30 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0020_alter_lactatingcow_cow_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='calf',
            name='dam_details',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='monthlymilkrecord',
            unique_together={('cow_name', 'month')},
        ),
    ]
