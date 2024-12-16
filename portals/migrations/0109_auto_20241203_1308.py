# Generated by Django 3.1.3 on 2024-12-03 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portals', '0108_monthlyreport_movementpermit_noobjection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlyreport',
            name='assigned_to',
            field=models.ForeignKey(default=1, limit_choices_to={'is_farmer': True}, on_delete=django.db.models.deletion.CASCADE, related_name='monthly_report', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='movementpermit',
            name='assigned_to',
            field=models.ForeignKey(default=1, limit_choices_to={'is_farmer': True}, on_delete=django.db.models.deletion.CASCADE, related_name='movement_permit', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='noobjection',
            name='assigned_to',
            field=models.ForeignKey(default=1, limit_choices_to={'is_farmer': True}, on_delete=django.db.models.deletion.CASCADE, related_name='noobjection_form', to=settings.AUTH_USER_MODEL),
        ),
    ]