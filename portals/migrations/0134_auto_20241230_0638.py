# Generated by Django 3.1.3 on 2024-12-30 06:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0133_auto_20241229_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='practitioner',
            name='epmloyment_status',
            field=models.CharField(choices=[('employed', 'Employed'), ('private_practitioner', 'Private Practitioneer ')], default='Employed', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='practitioner',
            name='reg_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
