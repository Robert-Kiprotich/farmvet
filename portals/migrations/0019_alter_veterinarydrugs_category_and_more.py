# Generated by Django 4.2.11 on 2024-07-09 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0018_veterinarydrugs_date_of_purchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='veterinarydrugs',
            name='category',
            field=models.CharField(choices=[('Antibiotics', 'Antibiotics '), ('Vaccines', 'Vaccines'), ('Hormones', 'Hormones'), ('Metabolics', 'Metabolics')], max_length=15, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='veterinarydrugs',
            name='date_of_purchase',
            field=models.DateField(max_length=40, verbose_name='Date of purchase'),
        ),
    ]
