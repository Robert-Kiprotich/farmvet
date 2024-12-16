# Generated by Django 3.1.3 on 2024-12-03 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portals', '0107_auto_20241203_0820'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoObjection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_confirmation', models.DateField()),
                ('sub_county_district', models.CharField(max_length=100)),
                ('ward_level', models.CharField(max_length=100)),
                ('confirmed_by', models.CharField(max_length=100)),
                ('registration_number', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('uploaded_no_objection_form', models.FileField(upload_to='no_objection_forms/')),
                ('assigned_to', models.ForeignKey(limit_choices_to={'is_farmer': True}, on_delete=django.db.models.deletion.CASCADE, related_name='noobjection_form', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MovementPermit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_permit', models.DateField()),
                ('sub_county_district', models.CharField(max_length=100)),
                ('ward_level', models.CharField(max_length=100)),
                ('authorized_by', models.CharField(max_length=100)),
                ('registration_number', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('uploaded_permit', models.FileField(upload_to='movement_permits/')),
                ('assigned_to', models.ForeignKey(limit_choices_to={'is_farmer': True}, on_delete=django.db.models.deletion.CASCADE, related_name='movement_permit', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MonthlyReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_submission', models.DateField()),
                ('sub_county', models.CharField(max_length=100)),
                ('ward_level', models.CharField(max_length=100)),
                ('submitted_by', models.CharField(max_length=100)),
                ('registration_number', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('uploaded_report', models.FileField(upload_to='monthly_reports/')),
                ('assigned_to', models.ForeignKey(limit_choices_to={'is_farmer': True}, on_delete=django.db.models.deletion.CASCADE, related_name='monthly_report', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]