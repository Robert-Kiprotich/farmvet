# Generated by Django 3.1.3 on 2024-12-17 09:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portals', '0120_auto_20241217_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artificialinsemination',
            name='assigned_to',
            field=models.ForeignKey(blank=True, default=1, limit_choices_to={'is_farmer': False}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ai_assign', to=settings.AUTH_USER_MODEL),
        ),
    ]