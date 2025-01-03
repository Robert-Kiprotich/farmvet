# Generated by Django 3.1.3 on 2024-12-17 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portals', '0122_auto_20241217_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccinationrecord',
            name='assigned_to',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_farmer': False}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vaccination', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vaccinationrecord',
            name='assigned_to_official',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_official': False}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vaccination_official', to=settings.AUTH_USER_MODEL),
        ),
    ]
