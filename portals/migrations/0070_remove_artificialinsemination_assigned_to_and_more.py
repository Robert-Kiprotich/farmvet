# Generated by Django 4.2.11 on 2024-11-05 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0069_section_tutorial_alter_choice_question_userprogress_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artificialinsemination',
            name='assigned_to',
        ),
        migrations.RemoveField(
            model_name='artificialinsemination',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='artificialinsemination',
            name='previous_calf_gender',
        ),
        migrations.RemoveField(
            model_name='artificialinsemination',
            name='served_by',
        ),
        migrations.AddField(
            model_name='artificialinsemination',
            name='farmer_name',
            field=models.CharField(default='jdjd', max_length=255),
            preserve_default=False,
        ),
    ]