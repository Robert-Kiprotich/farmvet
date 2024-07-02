# Generated by Django 4.2.11 on 2024-06-25 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portals', '0007_heatsignmonitoring_date_of_heat_monitoring_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calf',
            name='breeding_level',
            field=models.CharField(choices=[('Purebred', 'Purebred'), ('Crossbred', 'Crossbred'), ('MixedBreed', 'MixedBreed')], default='Purebreed', max_length=100),
        ),
        migrations.AlterField(
            model_name='lactatingcow',
            name='breeding_level',
            field=models.CharField(choices=[('Purebred', 'Purebred'), ('Crossbred', 'Crossbred'), ('MixedBreed', 'MixedBreed')], max_length=50),
        ),
        migrations.CreateModel(
            name='SalesOfMilk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_sales', models.DateField()),
                ('number_of_cows_milked', models.PositiveIntegerField()),
                ('total_kgs_milked', models.FloatField()),
                ('milk_sales_to', models.CharField(choices=[('Neighbour', 'Neighbour'), ('Hotel', 'Hotel'), ('Cooperative', 'Cooperative')], max_length=12)),
                ('buyer_contact', models.CharField(max_length=50)),
                ('price_per_kg', models.FloatField()),
                ('total_cash_received', models.FloatField()),
                ('balance', models.FloatField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]