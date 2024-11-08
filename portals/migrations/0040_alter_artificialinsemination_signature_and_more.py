# Generated by Django 4.2.11 on 2024-08-28 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portals', '0039_alter_vaccinationrecord_signature_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artificialinsemination',
            name='signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='artificialinsemination',
            name='stamp',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='deworming',
            name='signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='deworming',
            name='stamp',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='farmconsultation',
            name='signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='farmconsultation',
            name='stamp',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='postmortemrecord',
            name='signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='postmortemrecord',
            name='stamp',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pregnancydiagnosis',
            name='signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pregnancydiagnosis',
            name='stamp',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='referral',
            name='signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='referral',
            name='stamp',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='samplecollection',
            name='signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='samplecollection',
            name='stamp',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sampleprocessing',
            name='signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sampleprocessing',
            name='stamp',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='surgicalrecord',
            name='signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='surgicalrecord',
            name='stamp',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vaccinationrecord',
            name='signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vaccinationrecord',
            name='stamp',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='veterinarybilling',
            name='signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='veterinarybilling',
            name='stamp',
            field=models.TextField(blank=True, null=True),
        ),
    ]