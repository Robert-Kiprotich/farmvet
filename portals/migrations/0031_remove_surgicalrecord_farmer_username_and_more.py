# Generated by Django 4.2.11 on 2024-08-22 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portals', '0030_alter_livestockincident_morbidity_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surgicalrecord',
            name='farmer_username',
        ),
        migrations.AddField(
            model_name='surgicalrecord',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='VaccinationRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animal_species_targeted', models.CharField(choices=[('Cattle', 'Cattle'), ('Sheep', 'Sheep'), ('Goat', 'Goat'), ('Donkey', 'Donkey'), ('Dog', 'Dog'), ('Horse', 'Horse'), ('Poultry', 'Poultry'), ('Other', 'Other')], max_length=20)),
                ('other_species', models.CharField(blank=True, max_length=255, null=True)),
                ('number_of_animals_vaccinated', models.IntegerField()),
                ('age_of_animal', models.CharField(max_length=50)),
                ('sex_of_animal', models.CharField(max_length=10)),
                ('breed_of_animal', models.CharField(max_length=100)),
                ('color_of_animal', models.CharField(max_length=100)),
                ('other_description', models.TextField(blank=True, null=True)),
                ('vaccination_of', models.CharField(max_length=255)),
                ('vaccines_used', models.CharField(max_length=255)),
                ('batch_number', models.CharField(max_length=255)),
                ('date_of_vaccination', models.DateField()),
                ('vaccination_type', models.CharField(choices=[('Primary', 'Primary'), ('Booster', 'Booster')], max_length=10)),
                ('next_date_of_vaccination', models.DateField()),
                ('name_of_rash', models.CharField(blank=True, max_length=255, null=True)),
                ('village_vaccination_done', models.CharField(blank=True, max_length=255, null=True)),
                ('nature_of_vaccination_program', models.CharField(choices=[('Mass', 'Mass'), ('Individual', 'Individual')], max_length=10)),
                ('name_of_owner', models.CharField(max_length=255)),
                ('village', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=50)),
                ('name_of_vet_incharge', models.CharField(max_length=255)),
                ('registration_number', models.CharField(max_length=255)),
                ('mobile_number', models.CharField(max_length=20)),
                ('vet_signature', models.CharField(max_length=255)),
                ('stamp_line', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostMortemRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('livestock_category', models.CharField(choices=[('cattle', 'Cattle'), ('sheep', 'Sheep'), ('goat', 'Goat'), ('dog', 'Dog'), ('cat', 'Cat'), ('horse', 'Horse'), ('poultry', 'Poultry'), ('none', 'None')], max_length=10)),
                ('other_livestock', models.CharField(blank=True, max_length=100, null=True)),
                ('name_of_animal', models.CharField(max_length=100)),
                ('sex', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)),
                ('age', models.CharField(max_length=100)),
                ('case_history', models.TextField()),
                ('number_of_sick_animals', models.IntegerField()),
                ('number_of_dead', models.IntegerField()),
                ('morbidity_rate', models.CharField(max_length=100)),
                ('date_of_incidence', models.DateField()),
                ('time_of_incidence', models.TimeField()),
                ('signs_of_cadaver', models.TextField()),
                ('cadaver_open_for_pm', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3)),
                ('reasons_for_not_opening', models.TextField(blank=True, null=True)),
                ('major_pathological_conditions', models.TextField(blank=True, null=True)),
                ('sample_sent_to_lab', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3)),
                ('cause_of_death_notifiable', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3)),
                ('cause_of_death_zoonotic', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3)),
                ('precautions_if_zoonotic', models.TextField(blank=True, null=True)),
                ('cadaver_disposed_by', models.CharField(choices=[('burial', 'Burial'), ('burning', 'Burning')], max_length=7)),
                ('owner_name', models.CharField(max_length=100)),
                ('owner_village', models.CharField(max_length=100)),
                ('owner_mobile_number', models.CharField(max_length=15)),
                ('vet_in_charge_name', models.CharField(max_length=100)),
                ('vet_in_charge_registration_number', models.CharField(max_length=100)),
                ('vet_in_charge_mobile_number', models.CharField(max_length=15)),
                ('signature_and_stamp', models.CharField(max_length=255)),
                ('farmer_username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_mortem_records', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
