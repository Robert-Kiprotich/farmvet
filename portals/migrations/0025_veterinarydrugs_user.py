# Generated by Django 4.2.11 on 2024-08-10 07:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portals', '0024_remove_veterinarydrugs_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='veterinarydrugs',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
