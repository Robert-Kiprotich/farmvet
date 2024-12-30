# Generated by Django 3.1.3 on 2024-12-17 10:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portals', '0121_auto_20241217_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artificialinsemination',
            name='assigned_to',
            field=models.ForeignKey(blank=True, default=1, limit_choices_to={'is_farmer': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ai_assign', to=settings.AUTH_USER_MODEL),
        ),
    ]