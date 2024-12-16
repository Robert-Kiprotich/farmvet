# Generated by Django 3.1.3 on 2024-11-29 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portals', '0104_assessmentrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessmentrecord',
            name='assigned_to',
            field=models.ForeignKey(default=1, limit_choices_to={'is_farmer': True}, on_delete=django.db.models.deletion.CASCADE, related_name='assesment_report', to='user.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assessmentrecord',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='calvingrecord',
            name='assigned_to',
            field=models.ForeignKey(default=1, limit_choices_to={'is_farmer': True}, on_delete=django.db.models.deletion.CASCADE, related_name='calving_report', to='user.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='calvingrecord',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
