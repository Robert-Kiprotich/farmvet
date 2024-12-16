# Generated by Django 3.1.3 on 2024-11-19 06:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portals', '0088_auto_20241119_0629'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpdquestions',
            name='question_text',
            field=models.CharField(default='no nini', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cpdquestions',
            name='tutorial',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='portals.tutorial'),
        ),
        migrations.AddField(
            model_name='cpdquestions',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.user'),
            preserve_default=False,
        ),
    ]
