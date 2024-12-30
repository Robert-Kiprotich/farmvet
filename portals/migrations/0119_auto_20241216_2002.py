# Generated by Django 3.1.3 on 2024-12-16 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portals', '0118_auto_20241216_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccinationrecord',
            name='assigned_to',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_farmer': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vaccination', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vaccinationrecord',
            name='assigned_to_official',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_official': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vaccination_official', to=settings.AUTH_USER_MODEL),
        ),
    ]
