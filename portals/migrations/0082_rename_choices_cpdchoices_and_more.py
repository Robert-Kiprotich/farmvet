# Generated by Django 4.2.11 on 2024-11-12 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0081_remove_questions_is_multiple_choice_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Choices',
            new_name='CpdChoices',
        ),
        migrations.RenameModel(
            old_name='Questions',
            new_name='CpdQuestions',
        ),
    ]