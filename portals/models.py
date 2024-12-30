from django.db import models
from django.contrib.auth.models import User
from user.models import *
from datetime import timedelta, date
from django.contrib import admin


BREEDING_LEVEL_CHOICES = [
		('Purebred', 'Purebred'),
		('Crossbred', 'Crossbred'),
		('MixedBreed', 'MixedBreed'),
	]


SEX_CHOICES = (
 	('Male','Male'),
 	('Female','Female')
 )


farmers_list = []


class VaccinationRecord(models.Model):
    
	CATTLE = 'Cattle'
	SHEEP = 'Sheep'
	GOAT = 'Goat'
	DONKEY = 'Donkey'
	DOG = 'Dog'
	HORSE = 'Horse'
	POULTRY = 'Poultry'
	OTHER = 'Other'

	ANIMAL_SPECIES_CHOICES = [
		(CATTLE, 'Cattle'),
		(SHEEP, 'Sheep'),
		(GOAT, 'Goat'),
		(DONKEY, 'Donkey'),
		(DOG, 'Dog'),
		(HORSE, 'Horse'),
		(POULTRY, 'Poultry'),
		(OTHER, 'Other'),
	]

	PRIMARY = 'Primary'
	BOOSTER = 'Booster'

	VACCINATION_TYPE_CHOICES = [
		(PRIMARY, 'Primary'),
		(BOOSTER, 'Booster'),
	]

	MASS = 'Mass'
	INDIVIDUAL = 'Individual'

	NATURE_OF_VACCINATION_PROGRAM_CHOICES = [
		(MASS, 'Mass'),
		(INDIVIDUAL, 'Individual'),
	]
	VACCINATION_SEX=[
		('Male','Male'),
		('Female','Female'),
		('All','All')

	]

	DISEASE_CHOICES = [
	('anthrax', 'Anthrax'),
	('fmd', 'FMD'),
	('lumpy_skin_disease', 'Lumpy Skin Disease'),
	('rift_valley_fever', 'Rift Valley Fever'),
	('rabies', 'Rabies'),
	('cbpp', 'CBPP '),
	('ccpp', 'CCPP '),
	('ppr', 'PPR '),
	('newcastle_disease', 'Newcastle Disease'),
	('canine_distemper', 'Canine Distemper'),
	('none', 'None'),
	]

    # Fields
    
	user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
	assigned_to = models.ForeignKey(
		User,
		on_delete=models.CASCADE,  
		related_name='vaccination',
		limit_choices_to={'is_farmer': False},
		null=True,                 
		blank=True,               
							
	)
	assigned_to_official = models.ForeignKey(
		User,
		on_delete=models.CASCADE,  
		related_name='vaccination_official',
		limit_choices_to={'is_official': False},
		null=True,                 
		blank=True,               
							
	)
	species_targeted = models.CharField(max_length=20,choices=ANIMAL_SPECIES_CHOICES)
	other_species = models.CharField(max_length=255, blank=True, null=True)
	number_of_animals_vaccinated = models.IntegerField()
	age_of_animal = models.CharField(max_length=50)
	sex_of_animal = models.CharField(max_length=10,choices=VACCINATION_SEX)
	breed_of_animal = models.CharField(max_length=100)
	color_of_animal = models.CharField(max_length=100)
	other_description = models.TextField(blank=True, null=True)
	vaccination_of = models.CharField(max_length=20,choices=DISEASE_CHOICES)
	other_disease=models.CharField(max_length=255)
	vaccines_used = models.CharField(max_length=255)
	batch_number = models.CharField(max_length=255)
	dosage = models.CharField(max_length=255)
	expiry_date = models.DateField()
	date_of_vaccination = models.DateField()
	vaccination_type = models.CharField(max_length=10,choices=VACCINATION_TYPE_CHOICES)
	next_date_of_vaccination = models.DateField()
	name_of_rash = models.CharField(max_length=255, blank=True, null=True)
	village_vaccination_done = models.CharField(max_length=255, blank=True, null=True)
	nature_of_vaccination_program = models.CharField(max_length=10,choices=NATURE_OF_VACCINATION_PROGRAM_CHOICES)
	name_of_owner = models.CharField(max_length=255)
	sub_county=models.CharField(max_length=255)
	ward=models.CharField(max_length=255)
	village = models.CharField(max_length=255)
	contact = models.CharField(max_length=50)
	name_of_vet_incharge = models.CharField(max_length=255)
	registration_number = models.CharField(max_length=255)
	mobile_number = models.CharField(max_length=20)
	signature = models.TextField(blank=True,null=True)

    
	def __str__(self):
		return f"Vaccination Record for {self.user} - {self.animal_species_targeted}"


class SurgicalRecord(models.Model):
	LIVESTOCK_CATEGORIES = [
		('Cattle', 'Cattle'),
		('Sheep', 'Sheep'),
		('Goat', 'Goat'),
		('Donkey', 'Donkey'),
		('Dog', 'Dog'),
		('Cat', 'Cat'),
		('Poultry', 'Poultry'),
		('None', 'None')
	]

	SEX_CHOICES = [
		('Male', 'Male'),
		('Female', 'Female')
	]

	AGE_CHOICES = [
		('Young', 'Young'),
		('Adult', 'Adult')
	]

	NATURE_OF_SURGERY = [
		('Emergency', 'Emergency'),
		('Elective', 'Elective')
	]

	TYPE_OF_SURGERY = [
		('C-section', 'C-section'),
		('Interstinal Torsion', 'Interstinal Torsion'),
		('Tumor Extraction', 'Tumor Extraction'),
		('Canine Spaying', 'Canine Spaying'),
		('Hernia', 'Hernia'),
		('Warts Extraction', 'Warts Extraction'),
		('Skin Repairs', 'Skin Repairs'),
		('Castration', 'Castration'),
		('Fracture Correction', 'Fracture Correction'),
		('Rumenotomy', 'Rumenotomy'),
		('None', 'None')
	]

	STATUS_CHOICES = [
		('Good', 'Good'),
		('Dehydrated', 'Dehydrated'),
		('Weak', 'Weak')
	]

	PROGNOSIS_CHOICES = [
		('Good', 'Good'),
		('Fair', 'Fair'),
		('Grave', 'Grave')
	]

	user = models.ForeignKey(User,on_delete=models.CASCADE,default=1,limit_choices_to={'is_vet_officer': True})
	assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='surgical_records', limit_choices_to={'is_farmer': True})
	livestock_category_affected = models.CharField(max_length=10, choices=LIVESTOCK_CATEGORIES)
	other_livestock_category = models.CharField(max_length=100, blank=True, null=True)
	name_of_animal = models.CharField(max_length=100)
	registration_number = models.CharField(max_length=100)
	sex_of_animal = models.CharField(max_length=6, choices=SEX_CHOICES)
	age_of_animal = models.CharField(max_length=5, choices=AGE_CHOICES)
	nature_of_surgery = models.CharField(max_length=10, choices=NATURE_OF_SURGERY)
	type_of_surgery = models.CharField(max_length=50, choices=TYPE_OF_SURGERY)
	other_surgery = models.CharField(max_length=100, blank=True, null=True)
	status_before_operation = models.CharField(max_length=15, choices=STATUS_CHOICES)
	pre_operative_management = models.TextField(blank=True, null=True)
	date_of_operation = models.DateField()
	post_operation_management = models.TextField(blank=True, null=True)
	prognosis_of_patient = models.CharField(max_length=15, choices=PROGNOSIS_CHOICES)
	comment = models.TextField(blank=True, null=True)
	owner_name = models.CharField(max_length=100)
	owner_village = models.CharField(max_length=100)
	owner_mobile_number = models.CharField(max_length=15)
	vet_in_charge = models.CharField(max_length=100)
	vet_registration_number = models.CharField(max_length=100)
	vet_mobile_number = models.CharField(max_length=15)
	signature = models.TextField(blank=True,null=True)
	stamp = models.TextField(blank=True,null=True)


	def __str__(self):
		return f"Surgical Record of {self.name_of_animal} ({self.registration_number})"

class SampleCollection(models.Model):
	LIVESTOCK_CATEGORY_CHOICES = [
		('cattle', 'Cattle'),
		('sheep', 'Sheep'),
		('goat', 'Goat'),
		('dog', 'Dog'),
		('cat', 'Cat'),
		('horse', 'Horse'),
		('poultry', 'Poultry'),
		('none', 'None'),
	]

	SEX_CHOICES = [
		('male', 'Male'),
		('female', 'Female'),
	]

	AGE_CHOICES = [
		('young', 'Young'),
		('adult', 'Adult'),
	]

	SAMPLE_TYPE_CHOICES = [
		('milk', 'Milk'),
		('blood_smear', 'Blood Smear'),
		('lymph_node_smear', 'Lymph Node Smear'),
		('urine', 'Urine'),
		('faeces', 'Faeces'),
		('ear_notching', 'Ear Notching'),
		('biopsy', 'Biopsy'),
		('skin_scraping', 'Skin Scraping'),
		('vaginal_swap', 'Vaginal Swap'),
		('head', 'Head'),
	]

	SAMPLE_RATING_CHOICES = [
		('highly_infectious', 'Highly Infectious'),
		('not_infectious', 'Not Infectious'),
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
	assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collection_records', limit_choices_to={'is_farmer': True})
	livestock_category = models.CharField(max_length=10, choices=LIVESTOCK_CATEGORY_CHOICES)
	other_livestock = models.CharField(max_length=100, blank=True, null=True)
	name_of_animal = models.CharField(max_length=100)
	registration_number = models.CharField(max_length=100)
	age_of_animal = models.CharField(max_length=10, choices=AGE_CHOICES)
	sex_of_animal = models.CharField(max_length=6, choices=SEX_CHOICES)
	history_of_animal = models.TextField()
	clinical_signs_of_animal = models.TextField()
	type_of_sample_collected = models.CharField(max_length=20, choices=SAMPLE_TYPE_CHOICES)
	date_of_sampling = models.DateField()
	sample_storage_condition = models.CharField(max_length=100)
	means_of_transportation = models.CharField(max_length=100)
	sample_rating = models.CharField(max_length=20, choices=SAMPLE_RATING_CHOICES)
	owner_name = models.CharField(max_length=100)
	owner_village = models.CharField(max_length=100)
	owner_mobile_number = models.CharField(max_length=15)
	vet_in_charge_name = models.CharField(max_length=100)
	vet_in_charge_registration_number = models.CharField(max_length=100)
	vet_in_charge_mobile_number = models.CharField(max_length=15)
	signature = models.TextField(blank=True,null=True)
	stamp = models.TextField(blank=True,null=True)

	def __str__(self):
		return f"{self.name_of_animal} - {self.livestock_category} ({self.date_of_sampling})"



class SampleProcessing(models.Model):
	LIVESTOCK_CATEGORY_CHOICES = [
		('cattle', 'Cattle'),
		('sheep', 'Sheep'),
		('goat', 'Goat'),
		('dog', 'Dog'),
		('cat', 'Cat'),
		('horse', 'Horse'),
		('poultry', 'Poultry'),
		('none', 'None'),
	]

	SEX_CHOICES = [
		('male', 'Male'),
		('female', 'Female'),
	]

	AGE_CHOICES = [
		('young', 'Young'),
		('adult', 'Adult'),
	]

	SAMPLE_RATING_CHOICES = [
		('highly_infectious', 'Highly Infectious'),
		('not_infectious', 'Not Infectious'),
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processing_records', limit_choices_to={'is_farmer': True})
	livestock_category = models.CharField(max_length=10, choices=LIVESTOCK_CATEGORY_CHOICES)
	sample_type_received = models.CharField(max_length=255)
	sample_rating = models.CharField(max_length=20, choices=SAMPLE_RATING_CHOICES)
	animal_name = models.CharField(max_length=100)
	registration_number = models.CharField(max_length=100)
	sex_of_animal = models.CharField(max_length=6, choices=SEX_CHOICES)
	age_of_animal = models.CharField(max_length=10, choices=AGE_CHOICES)
	date_of_reception = models.DateField()
	date_of_sample_processing = models.DateField()
	number_of_days_for_processing = models.IntegerField()
	date_of_sample_results = models.DateField()
	laboratory_findings = models.TextField()
	comment = models.TextField(blank=True, null=True)
	owner_name = models.CharField(max_length=100)
	owner_village = models.CharField(max_length=100)
	owner_mobile_number = models.CharField(max_length=15)
	lab_technologist_name = models.CharField(max_length=100)
	lab_technologist_registration_number = models.CharField(max_length=100)
	lab_technologist_mobile_number = models.CharField(max_length=15)
	laboratory_name = models.CharField(max_length=100)
	signature = models.TextField(blank=True,null=True)
	stamp = models.TextField(blank=True,null=True)

	def __str__(self):
		return f"{self.name_of_animal} - {self.livestock_category} ({self.date_of_reception})"


class LaboratoryRecord(models.Model):
    LIVESTOCK_CATEGORY_CHOICES = [
        ('cattle', 'Cattle'),
        ('sheep', 'Sheep'),
        ('goat', 'Goat'),
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('horse', 'Horse'),
        ('poultry', 'Poultry'),
        ('none', 'None'),
    ]

    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    AGE_CHOICES = [
        ('young', 'Young'),
        ('adult', 'Adult'),
    ]

    SAMPLE_TYPE_CHOICES = [
        ('milk', 'Milk'),
        ('blood_smear', 'Blood Smear'),
        ('lymph_node_smear', 'Lymph Node Smear'),
        ('urine', 'Urine'),
        ('faeces', 'Faeces'),
        ('cfs', 'CFS'),
        ('biopsy', 'Biopsy'),
        ('skin_scraping', 'Skin Scraping'),
        ('vaginal_swap', 'Vaginal Swap'),
        ('head', 'Head'),
    ]

    SAMPLE_RATING_CHOICES = [
        ('highly_infectious', 'Highly Infectious'),
        ('not_infectious', 'Not Infectious'),
    ]

    TRANSPORTATION_CHOICES = [
        ('vehicle', 'Vehicle'),
        ('motorbike', 'Motorbike'),
        ('footing', 'Footing'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lab_records', limit_choices_to={'is_farmer': True})
    livestock_category = models.CharField(max_length=10, choices=LIVESTOCK_CATEGORY_CHOICES)
    other_livestock = models.CharField(max_length=100, blank=True, null=True)
    name_of_animal = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100)
    age_of_animal = models.CharField(max_length=10, choices=AGE_CHOICES)
    sex_of_animal = models.CharField(max_length=6, choices=SEX_CHOICES)
    history_of_animal = models.TextField()
    clinical_signs = models.TextField()
    type_of_sample_collected = models.CharField(max_length=20, choices=SAMPLE_TYPE_CHOICES)
    date_of_sampling = models.DateField()
    sample_storage_condition = models.CharField(max_length=255)
    means_of_transportation = models.CharField(max_length=10, choices=TRANSPORTATION_CHOICES)
    sample_rating = models.CharField(max_length=20, choices=SAMPLE_RATING_CHOICES)
    owner_name = models.CharField(max_length=100)
    owner_village = models.CharField(max_length=100)
    owner_mobile_number = models.CharField(max_length=15)
    vet_in_charge_name = models.CharField(max_length=100)
    vet_registration_number = models.CharField(max_length=100)
    vet_mobile_number = models.CharField(max_length=15)
    signature = models.CharField(max_length=255)
    stamp = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name_of_animal} - {self.livestock_category} ({self.date_of_sampling})"



class LivestockIncident(models.Model):
    LIVESTOCK_CATEGORY_CHOICES = [
        ('cattle', 'Cattle'),
        ('sheep', 'Sheep'),
        ('goat', 'Goat'),
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('horse', 'Horse'),
        ('poultry', 'Poultry'),
    ]

    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    DISPOSAL_WAY_CHOICES = [
        ('burial', 'Burial'),
        ('cremation', 'Cremation'),
    ]

    
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incidence_records', limit_choices_to={'is_farmer': True})
    livestock_category = models.CharField(max_length=10, choices=LIVESTOCK_CATEGORY_CHOICES)
    animal_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    age = models.PositiveIntegerField()
    case_history = models.TextField()
    number_of_sick_animals = models.PositiveIntegerField()
    morbidity_rate = models.CharField(blank=True,max_length=40)
    incidence_date = models.DateField()
    incidence_time = models.TimeField()
    cadaver_signs = models.TextField()
    open_for_pm = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    no_pm_reason = models.TextField(blank=True, null=True)
    path_condition = models.TextField()
    sample_sent = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    cause_notifiable = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    cause_zoonotic = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    precaution = models.TextField()
    disposal_way = models.CharField(max_length=10, choices=DISPOSAL_WAY_CHOICES)

    def __str__(self):
        return f"{self.animal_name} - {self.livestock_category} ({self.incidence_date})"


class Referral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_records', limit_choices_to={'is_farmer': True})
    species = models.CharField(max_length=255)  
    treatment_duration = models.CharField(max_length=255)  
    previous_treatment_state = models.TextField()  
    prognosis = models.TextField()  
    referral_date = models.DateField()  
    referral_choice = models.CharField(max_length=255)  
    r_vet_name = models.CharField(max_length=255)  
    r_vet_contact = models.CharField(max_length=15)  
    r_vet_reg_no = models.CharField(max_length=255)  
    farmer_name = models.CharField(max_length=255)
    village = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)  
    vet_name = models.CharField(max_length=255)  
    vet_reg_no = models.CharField(max_length=255)  
    vet_contact = models.CharField(max_length=15)  
    signature = models.TextField(blank=True,null=True)
    stamp = models.TextField(blank=True,null=True)
    comment = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"Referral for {self.species} by {self.vet_name} on {self.referral_date}"

class FarmConsultation(models.Model):
    DAIRY = 'Dairy'
    BEEF_PRODUCTION = 'Beef Production'
    POULTRY_PRODUCTION = 'Poultry Production'
    GOAT_PRODUCTION = 'Goat Production'
    PETS = 'Pets'
    OTHER = 'Other'

    AREA_OF_INTEREST_CHOICES = [
        (DAIRY, 'Dairy'),
        (BEEF_PRODUCTION, 'Beef Production'),
        (POULTRY_PRODUCTION, 'Poultry Production'),
        (GOAT_PRODUCTION, 'Goat Production'),
        (PETS, 'Pets'),
        (OTHER, 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultation_records', limit_choices_to={'is_farmer': True})
    area_of_interest = models.CharField(max_length=20, choices=AREA_OF_INTEREST_CHOICES)
    other = models.CharField(max_length=255, blank=True, null=True) 
    recommendation = models.TextField(blank=True, null=True)  
    other_area_of_interest = models.CharField(max_length=255, blank=True, null=True) 
    give_recommendation = models.TextField(blank=True, null=True) 
    manager = models.CharField(max_length=255)  
    consultant = models.CharField(max_length=255)  
    farmer_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)  
    village = models.CharField(max_length=255)
    vet_name = models.CharField(max_length=255)
    vet_reg_no = models.CharField(max_length=255) 
    vet_contact = models.CharField(max_length=15)  
    signature = models.TextField(blank=True,null=True)
    stamp = models.TextField(blank=True,null=True)
    comment = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"{self.farmer_name} - {self.area_of_interest} - {self.vet_name}"

class PregnancyDiagnosis(models.Model):
    ADULT = 'Adult'
    HEIFER = 'Heifer'
    CATEGORY_CHOICES = [
        (ADULT, 'Adult'),
        (HEIFER, 'Heifer'),
    ]

    POSITIVE = 'Positive'
    NEGATIVE = 'Negative'
    NOT_CONFIRMED = 'Not Confirmed'
    PD_RESULTS_CHOICES = [
        (POSITIVE, 'Positive'),
        (NEGATIVE, 'Negative'),
        (NOT_CONFIRMED, 'Not Confirmed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pregdiagnosis_records', limit_choices_to={'is_farmer': True})
    cow_name = models.CharField(max_length=255)
    reg_no = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    date_of_ai = models.DateField()  # Date of Artificial Insemination
    pg_diag_date = models.DateField()  # Pregnancy diagnosis date
    pd_results = models.CharField(max_length=15, choices=PD_RESULTS_CHOICES)
    pd_method = models.CharField(max_length=255)  # Method used for pregnancy diagnosis
    positive_pd_months = models.IntegerField(blank=True, null=True)  # Number of months if positive
    negative_pd_comment = models.TextField(blank=True, null=True)  # Comments if negative
    pd_nxt_date = models.DateField(blank=True, null=True)  # Next pregnancy diagnosis date
    expctd_delivery_date = models.DateField(blank=True, null=True)  # Expected delivery date
    comment = models.TextField(blank=True, null=True)  # Additional comments
    owners_name = models.CharField(max_length=255)
    village = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)  # Adjust max_length as necessary
    vet_name = models.CharField(max_length=255)
    vet_reg_no = models.CharField(max_length=255)  # Vet's registration number
    vet_contact = models.CharField(max_length=15)  # Adjust max_length as necessary
    signature = models.TextField(blank=True,null=True)
    stamp = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.cow_name} - {self.reg_no} - {self.pd_results}"

class PostMortemRecord(models.Model):
    LIVESTOCK_CATEGORY_CHOICES = [
        ('cattle', 'Cattle'),
        ('sheep', 'Sheep'),
        ('goat', 'Goat'),
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('horse', 'Horse'),
        ('poultry', 'Poultry'),
        ('none', 'None'),
    ]

    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    DISPOSAL_CHOICES = [
        ('burial', 'Burial'),
        ('burning', 'Burning'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postmortem_records', limit_choices_to={'is_farmer': True})
    livestock_category = models.CharField(max_length=10, choices=LIVESTOCK_CATEGORY_CHOICES)
    other_livestock = models.CharField(max_length=100, blank=True, null=True)
    name_of_animal = models.CharField(max_length=100)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    age = models.CharField(max_length=100)
    case_history = models.TextField()
    number_of_sick_animals = models.IntegerField()
    number_of_dead = models.IntegerField()
    morbidity_rate = models.CharField(max_length=100)
    date_of_incidence = models.DateField()
    time_of_incidence = models.TimeField()
    signs_of_cadaver = models.TextField()
    cadaver_open_for_pm = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    reasons_for_not_opening = models.TextField(blank=True, null=True)
    major_pathological_conditions = models.TextField(blank=True, null=True)
    sample_sent_to_lab = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    cause_of_death_notifiable = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    cause_of_death_zoonotic = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    precautions_if_zoonotic = models.TextField(blank=True, null=True)
    cadaver_disposed_by = models.CharField(max_length=7, choices=DISPOSAL_CHOICES)
    owner_name = models.CharField(max_length=100)
    owner_village = models.CharField(max_length=100)
    owner_mobile_number = models.CharField(max_length=15)
    vet_in_charge_name = models.CharField(max_length=100)
    vet_in_charge_registration_number = models.CharField(max_length=100)
    vet_in_charge_mobile_number = models.CharField(max_length=15)
    signature = models.TextField(blank=True,null=True)
    stamp = models.TextField(blank=True,null=True)


    def __str__(self):
        return f"Post Mortem Record - {self.name_of_animal} ({self.date_of_incidence})"

class VeterinaryBilling(models.Model):
    DEWORMING = 'Deworming'
    SURGERY = 'Surgery'
    AI = 'AI'
    CLINICAL = 'Clinical'
    VACCINATION = 'Vaccination'
    POST_MORTEM = 'Post Mortem'
    PREGNANCY_DIAGNOSIS = 'Pregnancy Diagnosis'
    LAB_CHARGES = 'Lab Charges'

    BILLING_CATEGORY_CHOICES = [
        (DEWORMING, 'Deworming'),
        (SURGERY, 'Surgery'),
        (AI, 'AI'),
        (CLINICAL, 'Clinical'),
        (VACCINATION, 'Vaccination'),
        (POST_MORTEM, 'Post Mortem'),
        (PREGNANCY_DIAGNOSIS, 'Pregnancy Diagnosis'),
        (LAB_CHARGES, 'Lab Charges'),
    ]

    CASH = 'Cash'
    CHEQUE = 'Cheque'
    MOBILE_MONEY = 'Mobile Money'
    BANK_TRANSFER = 'Bank Transfer'
    OTHER = 'Other'

    MODE_OF_PAYMENT_CHOICES = [
        (CASH, 'Cash'),
        (CHEQUE, 'Cheque'),
        (MOBILE_MONEY, 'Mobile Money'),
        (BANK_TRANSFER, 'Bank Transfer'),
        (OTHER, 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vet_billing_records', limit_choices_to={'is_farmer': True})
    billing_category = models.CharField(max_length=20, choices=BILLING_CATEGORY_CHOICES)
    total_amount_billed = models.DecimalField(max_digits=10, decimal_places=2)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2) 
    mode_of_payment = models.CharField(max_length=20, choices=MODE_OF_PAYMENT_CHOICES)
    agreed_date = models.DateField() 
    payment_plan = models.TextField(blank=True, null=True)  
    farmer_name = models.CharField(max_length=255)
    village = models.CharField(max_length=255)
    contact = models.CharField(max_length=15) 
    vet_to_be_paid = models.CharField(max_length=255) 
    reg_no = models.CharField(max_length=255)  
    vet_contact = models.CharField(max_length=15)  
    signature = models.TextField(blank=True, null=True)
    stamp = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True) 

    def save(self, *args, **kwargs):
      
        self.balance = self.total_amount_billed - self.total_paid
        super(VeterinaryBilling, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.farmer_name} - {self.billing_category} - {self.agreed_date}"
    
class Deworming(models.Model):
	CATTLE = 'Cattle'
	SHEEP = 'Sheep'
	GOAT = 'Goat'
	DONKEY = 'Donkey'
	DOG = 'Dog'
	HORSE = 'Horse'
	POULTRY = 'Poultry'
	OTHER = 'Other'

	SPECIES_TARGETED_CHOICES = [
		(CATTLE, 'Cattle'),
		(SHEEP, 'Sheep'),
		(GOAT, 'Goat'),
		(DONKEY, 'Donkey'),
		(DOG, 'Dog'),
		(HORSE, 'Horse'),
		(POULTRY, 'Poultry'),
		(OTHER, 'Other'),
	]
	user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deworming_records', limit_choices_to={'is_farmer': True})
	species_targeted = models.CharField(max_length=10, choices=SPECIES_TARGETED_CHOICES)
	other = models.CharField(max_length=255, blank=True, null=True)  # For specifying other species if "Other" is selected
	no_of_adults = models.IntegerField()
	no_of_young_ones = models.IntegerField()
	body_conditions = models.TextField()  # Description of the body condition of animals
	deworming_date = models.DateField()
	drug_of_choice = models.CharField(max_length=255)
	parasites = models.CharField(max_length=255)
	withdrawal_period = models.CharField(max_length=255)  # e.g., "7 days", "14 days"
	side_effects = models.TextField(blank=True, null=True)
	nxt_deworming_date = models.DateField()  # Next deworming date
	farmer_name = models.CharField(max_length=255)
	village = models.CharField(max_length=255)
	contact = models.CharField(max_length=15)  # Adjust max_length as necessary
	vet_name = models.CharField(max_length=255)
	reg_no = models.CharField(max_length=255)  # Vet registration number
	vet_contact = models.CharField(max_length=15)  # Adjust max_length as necessary
	signature = models.TextField(blank=True,null=True)
	stamp = models.TextField(blank=True,null=True)

	def __str__(self):
		return f"{self.farmer_name} - {self.deworming_date}"    

FARMERS = tuple(farmers_list)

class ArtificialInsemination(models.Model):
    
	SERVED_BY_CHOICES = [
	('AI', 'AI'),
	('BULL', 'Bull'),
	]
	ABORTION_STATUS_CHOICES = [
	('YES', 'Yes'),
	('NO', 'No'),
	]
	INSEMINATION_STATUS_CHOICES=[
		('First','First'),
		('Repeat','Repeat'),
	]
	SEMEN_TYPE=[
		('Conventional','Conventional'),
		('Sexed','Sexed'),
	]
	user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  
        related_name='ai_assign',
        limit_choices_to={'is_farmer': True},
        null=True,                 
        blank=True,
		editable=True,
        default=1                  
    )
	assigned_to_official = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  
        related_name='ai_official',
        limit_choices_to={'is_official': False},
        null=True,                 
        blank=True,
        editable=True,               
        default=1                  
    )
	farm_name = models.CharField(max_length=255)
	cow_name = models.CharField(max_length=255)
	reg_no = models.CharField(max_length=255)
	dam_details = models.TextField()
	sire_details = models.TextField()
	no_of_repeats = models.IntegerField()
	abortion_status = models.CharField(max_length=3, choices=ABORTION_STATUS_CHOICES)
	time_of_heat_sign = models.TimeField()
	date_of_heat_sign = models.DateField()
	insemination_date=models.DateField()
	insemination_time = models.TimeField()
	insemination_status=models.CharField(max_length=20,choices=INSEMINATION_STATUS_CHOICES)
	semen_type=models.CharField(max_length=20 ,choices=SEMEN_TYPE)
	breed_used = models.CharField(max_length=255)
	bull_name = models.CharField(max_length=255)
	bull_reg_no = models.CharField(max_length=255)
	semen_source = models.CharField(max_length=255)
	heat_sign_mtr_date = models.DateField()  
	repeat_heat_date = models.DateField()
	first_pd_date = models.DateField()  
	expected_delivery_date = models.DateField()
	owners_name = models.CharField(max_length=255)
	sub_county = models.CharField(max_length=25)
	ward = models.CharField(max_length=25)
	village = models.CharField(max_length=255)
	contact = models.CharField(max_length=15) 
	provided_by=models.CharField(max_length=255)
	vet_name = models.CharField(max_length=255)
	vet_reg_no = models.CharField(max_length=254)
	vet_contact = models.CharField(max_length=15)  
	signature_stamp = models.TextField(blank=True,null=True)
	

	def __str__(self):
		return f"{self.cow_name} - {self.reg_no}"

	def save(self, *args, **kwargs):
		if self.insemination_date:
			
			self.first_pd_date = self.insemination_date + timedelta(days=90)
			self.heat_sign_mtr_date=self.insemination_date + timedelta(days=15)
			self.expected_delivery_date = self.insemination_date + timedelta(days=9 * 30)
			self.repeat_heat_date = self.insemination_date + timedelta(days=21)
		super().save(*args, **kwargs)
	
class Calf(models.Model):
	
	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	name_given = models.CharField(max_length=100, default='')
	registration_number = models.CharField(max_length=100, unique=True, default='')
	dam_details=models.CharField(max_length=100, default='')
	birth_date = models.DateField()
	breed = models.CharField(max_length=100, default='')
	gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='')
	sire_details = models.CharField(max_length=100, default='')
	color = models.CharField(max_length=100, default='')
	birth_weight = models.FloatField()
	medical_conditions = models.CharField(max_length=100, blank=True, default='')
	registration_date = models.DateField(null=True, blank=True)
	expected_weaning = models.DateField(null=True, blank=True)
	breeding_level = models.CharField(max_length=100, default="Purebreed", choices=BREEDING_LEVEL_CHOICES)
	comments = models.CharField(max_length=100, blank=True, default='')

	def __str__(self):
		return self.name +'-'+ str(self.id)

class DeadAnimal(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	name = models.CharField(max_length=30, default='')
	farm_name = models.CharField(max_length=100, default='')
	no_of_affected = models.FloatField(default=0)
	gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='')
	breed = models.CharField(max_length=100, default='')
	sickness_period = models.CharField(max_length=30, default='')
	cause_of_death = models.CharField(max_length=30, default='')
	death_date = models.DateField(null=True, blank=True)
	death_time = models.TimeField(null=True, blank=True)
	signs_before_death = models.CharField(max_length=200, null=True, blank=True, default='')
	postmortem_by_vet = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='')
	safety_precaution = models.CharField(max_length=30, choices=[('Burying', 'Burying'), ('Cremation', 'Cremation')], default='')
	comment = models.CharField(max_length=300, null=True, blank=True, verbose_name='comment', default='')

	def __str__(self):
		return self.name +'-'+ str(self.id)

class Culling(models.Model):
	CULLING_REASONS = [
		('Disease', 'Disease'),
		('Old age', 'Old age'),
		('Poor performance', 'Poor performance'),
		('Genetic defects', 'Genetic defects'),
		('Other', 'Other'),
	]
	CULLING_METHOD = [
		('Killing', 'Killing'),
		('Selling', 'Selling'),
	]

	ANIMAL_TYPE=[
		('Cow','Cow'),
		('Sheep','Sheep'),
		('Goat','Goat')
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	name = models.CharField(max_length=100, default='')
	reg_no = models.CharField(max_length=100, unique=True, default='')
	age = models.CharField(max_length=100, default='')
	gender = models.CharField(max_length=100, default='')
	animal_type=models.CharField(max_length=100, choices=ANIMAL_TYPE, default='')
	breed = models.CharField(max_length=100, default='')
	culling_method = models.CharField(max_length=100, choices=CULLING_METHOD, default='')
	no_of_culled = models.FloatField(default=0)
	culling_reason = models.CharField(max_length=100, choices=CULLING_REASONS, default='')
	culling_date = models.DateField()
	culling_price = models.DecimalField(max_digits=10, decimal_places=2)
	comment = models.TextField(blank=True, null=True, default='')

	def __str__(self):
		return self.name +'-'+ str(self.id)

class Livestock(models.Model):
	ANIMAL_TYPES = [
		('Cow', 'Cow'),
		('Goat', 'Goat'),
		('Sheep', 'Sheep'),
		('Pig', 'Pig'),
		('Chicken', 'Chicken'),
		# Add more types as needed
	]
	BREED_CHOICES = [
		('Dog', [
			('Labrador Retriever', 'Labrador Retriever'),
			('German Shepherd', 'German Shepherd'),
			('Golden Retriever', 'Golden Retriever'),
			('Bulldog', 'Bulldog'),
			('Beagle', 'Beagle'),
			('Poodle', 'Poodle'),
			('Boxer', 'Boxer'),
			('Dachshund', 'Dachshund'),
			('Yorkshire Terrier', 'Yorkshire Terrier'),
			('Rottweiler', 'Rottweiler'),
		]),
		('Cat', [
			('Siamese', 'Siamese'),
			('Persian', 'Persian'),
			('Maine Coon', 'Maine Coon'),
			('Ragdoll', 'Ragdoll'),
			('British Shorthair', 'British Shorthair'),
			('Sphynx', 'Sphynx'),
			('Bengal', 'Bengal'),
			('Abyssinian', 'Abyssinian'),
			('Scottish Fold', 'Scottish Fold'),
			('Burmese', 'Burmese'),
		]),
		('Horse', [
			('Thoroughbred', 'Thoroughbred'),
			('Quarter Horse', 'Quarter Horse'),
			('Arabian', 'Arabian'),
			('Appaloosa', 'Appaloosa'),
			('Paint Horse', 'Paint Horse'),
			('Morgan', 'Morgan'),
			('Tennessee Walking Horse', 'Tennessee Walking Horse'),
			('Friesian', 'Friesian'),
			('Pony of the Americas', 'Pony of the Americas'),
			('Miniature Horse', 'Miniature Horse'),
		]),
		('Cattle', [
			('Angus', 'Angus'),
			('Hereford', 'Hereford'),
			('Charolais', 'Charolais'),
			('Simmental', 'Simmental'),
			('Limousin', 'Limousin'),
			('Texas Longhorn', 'Texas Longhorn'),
			('Holstein', 'Holstein'),
			('Jersey', 'Jersey'),
			('Gelbvieh', 'Gelbvieh'),
			('Brahman', 'Brahman'),
		]),
		('Sheep', [
			('Merino', 'Merino'),
			('Dorper', 'Dorper'),
			('Suffolk', 'Suffolk'),
			('Rambouillet', 'Rambouillet'),
			('Hampshire', 'Hampshire'),
			('Shropshire', 'Shropshire'),
			('Dorset', 'Dorset'),
			('Cotswold', 'Cotswold'),
			('Lincoln', 'Lincoln'),
			('Targhee', 'Targhee'),
		]),
		('Goat', [
			('Boer', 'Boer'),
			('Nubian', 'Nubian'),
			('Saanen', 'Saanen'),
			('Angora', 'Angora'),
			('LaMancha', 'LaMancha'),
			('Alpine', 'Alpine'),
			('Toggenburg', 'Toggenburg'),
			('Kiko', 'Kiko'),
			('Spanish', 'Spanish'),
			('Pygmy', 'Pygmy'),
		]),
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	animal_type = models.CharField(max_length=50, choices=ANIMAL_TYPES, default='')
	breed_category = models.CharField(max_length=50, choices=BREED_CHOICES, default='')
	date_added = models.DateField()
	no_of_animals = models.FloatField(default=0)
	no_of_males = models.FloatField(default=0)
	no_of_females = models.FloatField(default=0)
	no_of_adults = models.FloatField(default=0)
	no_of_young = models.FloatField(default=0)
	no_of_dead = models.FloatField(default=0)
	reason_for_death = models.CharField(max_length=100, default='')
	comment = models.TextField(blank=True, null=True, default='')

	def __str__(self):
		return self.name + ' - ' + str(self.id)

class NewAnimal(models.Model):
	SOURCE_CHOICES = [
		('Market', 'Market'),
		('Farmer', 'Farmer'),
	]

	BREEDING_LEVEL_CHOICES = [
		('Purebred', 'Purebred'),
		('Crossbred', 'Crossbred'),
		('Mixed Breed', 'Mixed Breed'),
	]
    
	DEFECT_CHOICES = [
		('Yes', 'Yes'),
		('No', 'No'),
	]

	MEDICAL_HISTORY_CHOICES = [
		('Yes', 'Yes'),
		('No', 'No'),
	]

	ASSESSED_BY_VET_CHOICES = [
		('Yes', 'Yes'),
		('No', 'No'),
	]

	INSURED_CHOICES = [
		('Yes', 'Yes'),
		('No', 'No'),
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	name = models.CharField(max_length=100, default='')
	reg_no = models.CharField(max_length=100, default='')
	source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='')
	farmer_name = models.CharField(max_length=100, default='')
	animal_type = models.CharField(max_length=100, default='')
	breed = models.CharField(max_length=100, default='')
	breeding_level = models.CharField(max_length=100, choices=BREEDING_LEVEL_CHOICES, default='')
	defect = models.CharField(max_length=3, choices=DEFECT_CHOICES, default='')
	defect_reason = models.TextField(default='')
	animal_color = models.CharField(max_length=100, default='')
	market_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	medical_history = models.CharField(max_length=3, choices=MEDICAL_HISTORY_CHOICES, default='')
	assessed_by_vet = models.CharField(max_length=3, choices=ASSESSED_BY_VET_CHOICES, default='')
	insured = models.CharField(max_length=3, choices=INSURED_CHOICES, default='')
	insuring_company = models.CharField(max_length=100, default='')
	date_added = models.DateField(null=True, blank=True)

	def __str__(self):
		return self.name + '-' + str(self.id)


class AnimalSale(models.Model):
		BREED_CHOICES = [
		('Dog', [
		('Labrador Retriever', 'Labrador Retriever'),
		('German Shepherd', 'German Shepherd'),
		('Golden Retriever', 'Golden Retriever'),
		('Bulldog', 'Bulldog'),
		('Beagle', 'Beagle'),
		('Poodle', 'Poodle'),
		('Boxer', 'Boxer'),
		('Dachshund', 'Dachshund'),
		('Yorkshire Terrier', 'Yorkshire Terrier'),
		('Rottweiler', 'Rottweiler'),
		]),
		('Cat', [
		('Siamese', 'Siamese'),
		('Persian', 'Persian'),
		('Maine Coon', 'Maine Coon'),
		('Ragdoll', 'Ragdoll'),
		('British Shorthair', 'British Shorthair'),
		('Sphynx', 'Sphynx'),
		('Bengal', 'Bengal'),
		('Abyssinian', 'Abyssinian'),
		('Scottish Fold', 'Scottish Fold'),
		('Burmese', 'Burmese'),
		]),
		('Horse', [
		('Thoroughbred', 'Thoroughbred'),
		('Quarter Horse', 'Quarter Horse'),
		('Arabian', 'Arabian'),
		('Appaloosa', 'Appaloosa'),
		('Paint Horse', 'Paint Horse'),
		('Morgan', 'Morgan'),
		('Tennessee Walking Horse', 'Tennessee Walking Horse'),
		('Friesian', 'Friesian'),
		('Pony of the Americas', 'Pony of the Americas'),
		('Miniature Horse', 'Miniature Horse'),
		]),
		('Cattle', [
		('Angus', 'Angus'),
		('Hereford', 'Hereford'),
		('Charolais', 'Charolais'),
		('Simmental', 'Simmental'),
		('Limousin', 'Limousin'),
		('Texas Longhorn', 'Texas Longhorn'),
		('Holstein', 'Holstein'),
		('Jersey', 'Jersey'),
		('Gelbvieh', 'Gelbvieh'),
		('Brahman', 'Brahman'),
		]),
		('Sheep', [
		('Merino', 'Merino'),
		('Dorper', 'Dorper'),
		('Suffolk', 'Suffolk'),
		('Rambouillet', 'Rambouillet'),
		('Hampshire', 'Hampshire'),
		('Shropshire', 'Shropshire'),
		('Dorset', 'Dorset'),
		('Cotswold', 'Cotswold'),
		('Lincoln', 'Lincoln'),
		('Targhee', 'Targhee'),
		]),
		('Goat', [
		('Boer', 'Boer'),
		('Nubian', 'Nubian'),
		('Saanen', 'Saanen'),
		('Angora', 'Angora'),
		('LaMancha', 'LaMancha'),
		('Alpine', 'Alpine'),
		('Toggenburg', 'Toggenburg'),
		('Kiko', 'Kiko'),
		('Spanish', 'Spanish'),
		('Pygmy', 'Pygmy'),
		]),
		]
		user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
		number_sold = models.IntegerField()
		name = models.CharField(max_length=100)
		reg_no = models.CharField(max_length=100)
		date_sold=models.DateField()
		age = models.IntegerField()
		breed = models.CharField(max_length=100,choices=BREED_CHOICES, default='')
		sex = models.CharField(max_length=10,choices=SEX_CHOICES)
		weight = models.DecimalField(max_digits=10, decimal_places=2)
		selling_price = models.DecimalField(max_digits=10, decimal_places=2)
		reason = models.TextField()
		comment = models.TextField()

		def __str__(self):
			return self.name + ' - ' + str(self.id)



class HeatSignMonitoring(models.Model):
		STATUS_CHOICES = [
		('Adult', 'Adult'),
		('Heifer', 'Heifer'),
		]
		user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)		
		name = models.CharField(max_length=100)
		reg_no = models.CharField(max_length=20)
		status = models.CharField(max_length=10, choices=STATUS_CHOICES)
		date_of_heat_sign = models.DateField()
		date_of_heat_monitoring= models.DateField()
		exp_date_of_repeated_heat = models.DateField()
		reason_skip_monitoring = models.TextField(blank=True, null=True)

		def __str__(self):
			return self.name + ' - ' + str(self.id)

class PregnancyMonitoring(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
	name = models.CharField(max_length=100)
	reg_no = models.CharField(max_length=50)
	date_of_ai = models.DateField()
	exp_heat_date = models.DateField(null=True, blank=True)
	repeat_heat_date=models.DateField(null=True,blank=True)
	first_preg_diag_date = models.DateField(null=True, blank=True)
	# PD_STATUS_CHOICES = (
	#     ('positive', 'Positive'),
	#     ('negative', 'Negative'),
	# )
	#pd_status = models.CharField(max_length=20, choices=PD_STATUS_CHOICES)
	#approximate_preg_months = models.IntegerField()
	#vet_recommendation = models.TextField()
	#date_of_second_diag = models.DateField(null=True, blank=True)
	# FOETUS_STATUS_CHOICES = (
	#     ('progressive', 'Progressive'),
	#     ('non-progressive', 'Non-Progressive'),
	# )
	#foetus_status = models.CharField(max_length=20, choices=FOETUS_STATUS_CHOICES)
	#non_prog_reason = models.CharField(max_length=255, null=True, blank=True, default="")
	#action_to_take = models.CharField(max_length=255, null=True, blank=True, default="")
	steaming_up_date = models.DateField(null=True, blank=True)
	expected_dob = models.DateField(null=True, blank=True)
	#actual_date_of_delivery = models.DateField(null=True, blank=True)

	def __str__(self):
		return self.name + ' - ' + str(self.id)

	def save(self, *args, **kwargs):
		if self.date_of_ai:
			
			self.first_preg_diag_date = self.date_of_ai + timedelta(days=90)
			self.steaming_up_date = self.date_of_ai + timedelta(days=7 * 30)
			self.expected_dob = self.date_of_ai + timedelta(days=9 * 30)
			self.exp_heat_date = self.date_of_ai + timedelta(days=21)
			self.repeat_heat_date = self.date_of_ai + timedelta(days=15)
		super().save(*args, **kwargs)

class GestationMonitoring(models.Model):
    gestation_date = models.DateField()
    repeat_date = models.DateField(blank=True, null=True)
    expected_delivery_date = models.DateField(blank=True, null=True)


class Feeds(models.Model):
		FEED_TYPE_CHOICES = [
			('Dairy Meal', 'Dairy Meal'),
			('Wheat Bran', 'Wheat Bran'),
			('Maize Chaff', 'Maize Chaff'),
			('Sunflower', 'Sunflower'),
		]
		user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
		date_of_purchase = models.DateField('Date of Purchase')
		feed_type = models.CharField('Feed Type', max_length=15, choices=FEED_TYPE_CHOICES)
		company = models.CharField('Company', max_length=255)
		expiry_date = models.DateField('Expiry Date')
		quantity_purchased= models.CharField('Quantity purchased', max_length=255)
		trade_name= models.CharField('Trade Name', max_length=255)
		weight=models.CharField('Weight', max_length=255)
		cost = models.DecimalField('Cost', max_digits=10, decimal_places=2)
		comment = models.TextField('Comment', blank=True)

		def __str__(self):
			return self.date_of_purchase + ' - ' + str(self.id)
class Minerals(models.Model):
		MINERAL_TYPE_CHOICES = [
			('Dairy Lick', 'Dairy Lick'),
			('Stock Lick', 'Stock Lick'),
			('Dry Cow', 'Dry Cow'),
			('Joto', 'Joto'),
			('Calves Mineral', 'Calves Mineral')
		]
		user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
		date_of_purchase = models.DateField('Date of Purchase')
		mineral_type = models.CharField('Feed Type', max_length=15, choices=MINERAL_TYPE_CHOICES)
		quantity=models.CharField('Company', max_length=255)
		company = models.CharField('Company', max_length=255)
		expiry_date = models.DateField('Expiry Date')
		cost = models.DecimalField('Cost', max_digits=10, decimal_places=2)
		comment = models.TextField('Comment', blank=True)

		def __str__(self):
			return self.date_of_purchase + ' - ' + str(self.id)
		
class VeterinaryBills(models.Model):
		user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
		date_of_billing = models.DateField('Date of Billing')
		bill_category = models.CharField('Bill Category', max_length=20)
		amount = models.DecimalField('Amount', max_digits=10, decimal_places=2)
		amount_billed = models.DecimalField('Amount', max_digits=10, decimal_places=2)
		balance = models.DecimalField('Balance', max_digits=10, decimal_places=2)
		billing_details=models.CharField('Company', max_length=255)
		comment = models.TextField('Comment', blank=True)

		def save(self, *args, **kwargs):
		# Calculate the balance before saving
			self.balance = self.amount_billed - self.amount
			super(VeterinaryBills, self).save(*args, **kwargs)

		def __str__(self):
				return f"{self.amount_billed} - {self.id}"
		
class Archaricides(models.Model):
		user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
		date_of_purchase = models.DateField('Date of Purchase')
		chemical_name = models.CharField('Chemical Name', max_length=50)
		trade_name = models.CharField('Chemical Name', max_length=50)
		quantity=models.CharField('Quantity', max_length=255)
		company = models.CharField('Company', max_length=255)
		application_rate = models.CharField('Rate', max_length=255)
		expiry_date = models.DateField('Expiry Date')
		times_used=models.CharField('Frequency', max_length=255)
		cost = models.DecimalField('Cost', max_digits=10, decimal_places=2)
		comment = models.TextField('Comment', blank=True)

		def __str__(self):
			return self.date_of_purchase + ' - ' + str(self.id)
		
class DairyEquipment(models.Model):
		user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
		name=models.CharField('Name', max_length=40)
		date_of_purchase = models.DateField('Date of Purchase')
		quantity=models.CharField('quantity', max_length=255)
		equipment_type = models.CharField('Type', max_length=255)
		model_number=models.CharField('Model Number', max_length=255)
		company = models.CharField('Company', max_length=255)
		cost = models.DecimalField('Cost', max_digits=10, decimal_places=2)
		source=models.CharField('Source', max_length=255)
		comment = models.TextField('Comment', blank=True)

		def __str__(self):
			return self.date_of_purchase + ' - ' + str(self.id)

class DairyHygiene(models.Model):
		user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
		chemical_name=models.CharField('Chemical Name', max_length=255)
		trade_name=models.CharField('Trade Name', max_length=255)
		date_of_purchase = models.DateField('Date of Purchase')
		item_purchased = models.CharField('Item', max_length=255)
		company = models.CharField('Company', max_length=255)
		quantity=models.CharField('quantity', max_length=255)
		cost = models.DecimalField('Cost', max_digits=10, decimal_places=2)
		expiry_date = models.DateField('Expiry Date')
		comment = models.TextField('Comment', blank=True)

		def __str__(self):
			return self.chemical_name + ' - ' + str(self.id)
		

	
class LivestockInsurance(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	number_insured=models.DecimalField('Number Insured', max_digits=10, decimal_places=2)
	breed = models.CharField(max_length=50)
	animal_species=models.CharField(max_length=50)
	company=models.CharField('Company', max_length=255)
	mode_of_payment=models.CharField('Mode Of payment', max_length=255)
	payment_date= models.DateField('Payment Date')
	total=models.DecimalField('Total', max_digits=10, decimal_places=2)
	comment=models.TextField('Comment', blank=True)

	def __str__(self):
			return self.company + ' - ' + str(self.id)
	
class VeterinaryDrugs(models.Model):
	DRUG_TYPE_CHOICES = [
			('Antibiotics', 'Antibiotics '),
			('Vaccines', 'Vaccines'),
			('Hormones', 'Hormones'),
			('Metabolics', 'Metabolics'),
			
		]
	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	date_of_purchase=models.DateField('Date of purchase',max_length=40)
	name=models.CharField('Name', max_length=255)
	category=models.CharField('Category', max_length=15,choices=DRUG_TYPE_CHOICES)
	company=models.CharField('company', max_length=50)
	expiry_date=models.DateField('Expiry Date')
	strange_condition=models.CharField('Strange Condition', max_length=255)
	vet_reg=models.CharField('Vet Registration', max_length=255)
	cost=models.DecimalField('Number Insured', max_digits=10, decimal_places=2)
	comment=models.TextField('Comment', blank=True)

	def __str__(self):
			return self.name + ' - ' + str(self.id)
	
class Employees(models.Model):
	EMPLOYMENT_MODES = [
	('Full-Time', 'Full-Time'),
	('Part-Time', 'Part-Time'),
	('Contract', 'Contract'),
	('Internship', 'Internship'),
	]
	POSITION_CHOICES = [
        ('Milker', 'Milker'),
        ('Cleaner', 'Cleaner'),
        ('Animal caretaker', 'Animal caretaker'),
        ('Driver', 'Driver'),
        ('Veterinary officer', 'Veterinary officer'),
        ('Manager', 'Manager')
    ]
    

	PAYMENT_METHODS = [
	('Bank Transfer', 'Bank Transfer'),
	('Cash', 'Cash'),
	('Cheque', 'Cheque'),
	('Mobile Banking', 'Mobile Banking'),
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	employee_name = models.CharField(max_length=100)
	id_no = models.CharField(max_length=20, unique=True)
	phone_no = models.CharField(max_length=15)
	county = models.CharField(max_length=50)
	district = models.CharField(max_length=50)
	village = models.CharField(max_length=50)
	next_of_kin = models.CharField(max_length=100)
	next_of_kin_phone_no = models.CharField(max_length=15)
	chief_name = models.CharField(max_length=50)
	chief_phone_no = models.CharField(max_length=15)
	employee_position = models.CharField(max_length=50, choices=POSITION_CHOICES)
	salary = models.DecimalField(max_digits=10, decimal_places=2)
	payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS)
	bank_account = models.CharField(max_length=30, blank=True, null=True)
	mode_of_employment = models.CharField(max_length=20, choices=EMPLOYMENT_MODES)
	contract_rewal_period = models.IntegerField(help_text='Contract renewal period in months')

	def __str__(self):
		return self.employee_name
	

class Salaries(models.Model):
	PAYMENT_TYPE = [
		('Salary', 'Salary'),
		('Advance', 'Advance'),
		('Emergency', 'Emergency'),
		('Other', 'Other'),
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
	employee_name = models.ForeignKey(Employees, related_name='salaries_by_name', on_delete=models.CASCADE)
	employee_position = models.CharField(max_length=50, choices=Employees.POSITION_CHOICES)
	identification = models.CharField('identification', unique=True, max_length=255)
	mode_of_payment = models.CharField('Mode', max_length=255, choices=Employees.PAYMENT_METHODS)
	bank_account = models.CharField('Bank Account', max_length=255) 
	salary_amount = models.DecimalField('Amount', max_digits=10, decimal_places=2) # Change to CharField to store account number
	amount = models.DecimalField('Amount', max_digits=10, decimal_places=2)
	balance = models.DecimalField('Balance', max_digits=10, decimal_places=2)
	payment_date = models.DateField('Payment Date')
	payment_type = models.CharField('Type', max_length=255, choices=PAYMENT_TYPE)
	comment = models.TextField('Comment', blank=True)

	def __str__(self):
		return f"{self.employee_name} - {self.employee_position}"

	def save(self, *args, **kwargs):
		if self.employee_name_id:
			employee = Employees.objects.get(pk=self.employee_name_id)
			self.bank_account = employee.bank_account 

		self.balance=self.salary_amount - self.amount
		
		super().save(*args, **kwargs)	

class LactatingCow(models.Model):
	LACTATION_STAGE_CHOICES = [
		('early', 'Early'),
		('mid', 'Mid'),
		('late', 'Late'),
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	cow_name = models.CharField(max_length=100,unique=True)
	reg_no = models.CharField(max_length=50)
	sire_details = models.CharField(max_length=100)
	breed = models.CharField(max_length=50)
	breeding_level = models.CharField(max_length=50,choices=BREEDING_LEVEL_CHOICES)
	age = models.PositiveIntegerField(help_text="Age in years")
	calving_down_date = models.DateField()
	no_of_calves = models.PositiveIntegerField()
	average_daily_milk = models.FloatField(help_text="Average daily milk production in liters")
	lactation_stage = models.CharField(max_length=10, choices=LACTATION_STAGE_CHOICES)
	expected_date_of_drying_off = models.DateField()

	def __str__(self):
		return f"{self.cow_name} ({self.reg_no})"

class MilkRecord(models.Model):
	TIME_OF_MILKING_CHOICES = [
	('Morning', 'Morning'),
	('Noon', 'Noon'),
	('Evening', 'Evening'),
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	cow_name = models.ForeignKey(LactatingCow, on_delete=models.CASCADE,default=1)
	employee_name = models.ForeignKey(Employees, on_delete=models.CASCADE,default=2)
	date = models.DateField()
	time_of_milking = models.CharField(max_length=10, choices=TIME_OF_MILKING_CHOICES)
	quantity = models.FloatField(help_text="Amount of milk in liters")

	def __str__(self):
		return f"{self.date} - {self.cow_name} - {self.time_of_milking}"
	
	
class DailyMilkRecord(models.Model):
    cow_name = models.ForeignKey(LactatingCow, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    total_quantity = models.FloatField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)  
	

    def __str__(self):
        return f"{self.cow_name} - {self.date} {self.time}"

class WeeklyMilkRecord(models.Model):
	
	cow_name = models.ForeignKey(LactatingCow, on_delete=models.CASCADE)
	week_start_date = models.DateField()
	total_quantity = models.FloatField(help_text="Total milk in liters for the week")
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
	

	def __str__(self):
		return f"Week starting {self.week_start_date} - {self.cow_name}"

class MonthlyMilkRecord(models.Model):
	
	cow_name = models.ForeignKey(LactatingCow, on_delete=models.CASCADE)
	month = models.DateField()
	total_quantity = models.FloatField(help_text="Total milk in liters for the month")
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)

	class Meta:
		unique_together = ('cow_name', 'month')

	def __str__(self):
		return f"Month of {self.month.strftime('%B %Y')} - {self.cow_name}"
	

class SalesOfMilk(models.Model):
	MILK_SALES_TO = [
	('Neighbour', 'Neighbour'),
	('Hotel', 'Hotel'),
	('Cooperative', 'Cooperative'),
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	date_of_sales = models.DateField()
	number_of_cows_milked = models.PositiveIntegerField()
	total_kgs_milked = models.FloatField()
	milk_sales_to = models.CharField(max_length=12,choices=MILK_SALES_TO)
	buyer_contact = models.CharField(max_length=50)
	price_per_kg = models.FloatField()
	total_cash_received = models.FloatField()
	balance = models.FloatField(blank=True,null=True)
	comment = models.TextField(blank=True, null=True)

	def __str__(self):
		return f"Sales on {self.date_of_sales} to {self.milk_sales_to}"


class ClinicalRecord(models.Model):
	ANIMAL_SPECIES_CHOICES = [
		('Cattle', 'Cattle'),
		('Sheep', 'Sheep'),
		('Goat', 'Goat'),
		('Donkey', 'Donkey'),
		('Dog', 'Dog'),
		('Cat', 'Cat'),
		('Horse', 'Horse'),
		('Poultry', 'Poultry'),
		('Other', 'Other'),
	]

	DISEASE_NATURE_CHOICES = [
		('Acute', 'Acute'),
		('Sub-acute', 'Sub-acute'),
		('Chronic', 'Chronic'),
	]

	YES_NO_CHOICES = [
		('Yes', 'Yes'),
		('No', 'No'),
	]

	user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clinical_records', limit_choices_to={'is_farmer': True})
	animal_species_affected = models.CharField(max_length=20, choices=ANIMAL_SPECIES_CHOICES)
	other_species = models.CharField(max_length=100, blank=True, null=True)
	number_of_animals_sick = models.PositiveIntegerField()
	name_of_animal_affected = models.CharField(max_length=100)
	registration_number = models.CharField(max_length=100)
	age_of_animal = models.PositiveIntegerField()
	breed_of_animal = models.CharField(max_length=100)
	nature_of_disease = models.CharField(max_length=20, choices=DISEASE_NATURE_CHOICES)
	clinical_signs = models.TextField()
	differential_diagnosis = models.TextField()
	final_diagnosis = models.TextField()
	case_history = models.TextField()
	treatment_plan = models.TextField()
	drugs_of_choice = models.TextField()
	prognosis = models.TextField()
	date_of_start_dose = models.DateField()
	final_treatment_date = models.DateField(blank=True, null=True)
	is_zoonotic = models.CharField(max_length=3, choices=YES_NO_CHOICES)
	precautions = models.TextField(blank=True, null=True)
	refer_case_to_other_vet = models.CharField(max_length=3, choices=YES_NO_CHOICES)
	is_disease_reportable = models.CharField(max_length=3, choices=YES_NO_CHOICES)
	reason_if_not_reportable = models.TextField(blank=True, null=True)
	is_disease_notifiable = models.CharField(max_length=3, choices=YES_NO_CHOICES)
	notified_authority = models.CharField(max_length=3, choices=YES_NO_CHOICES)
	comment = models.TextField(blank=True, null=True)
	owner_name = models.CharField(max_length=100)
	owner_village = models.CharField(max_length=100)
	owner_contact = models.CharField(max_length=15)
	vet_in_charge_name = models.CharField(max_length=100)
	vet_registration_number = models.CharField(max_length=100)
	vet_contact = models.CharField(max_length=15)
	vet_signature = models.CharField(max_length=100)
	rubber_stamp = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return f"{self.farmer_username} - {self.name_of_animal_affected}"

class Client(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    date_of_enrollment = models.DateField()
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    livestock_interest = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name
    
    
    
class Diary(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    date = models.DateField()
    time_of_event=models.TimeField()
    main_activity = models.CharField(max_length=255)
    client_contact = models.CharField(max_length=15)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Diary Entry on {self.date} - {self.main_activity}"


class DiseaseReport(models.Model):
	LIVESTOCK_CATEGORY_CHOICES = [
		('cattle', 'Cattle'),
		('sheep', 'Sheep'),
		('goat', 'Goat'),
		('donkey', 'Donkey'),
		('dog', 'Dog'),
		('cat', 'Cat'),
		('poultry', 'Poultry'),
		('none', 'None'),
	]

	SEX_CHOICES = [
		('female', 'Female'),
		('male', 'Male'),
		('both', 'Both Female and Male'),
	]

	AGE_CHOICES = [
		('adult', 'Adult'),
		('young', 'Young'),
		('all', 'All'),
	]

	YES_NO_CHOICES = [
		('yes', 'Yes'),
		('no', 'No'),
	]
	user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	assigned_to_official = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disease_report', limit_choices_to={'is_official': True})
	livestock_category = models.CharField(max_length=20, choices=LIVESTOCK_CATEGORY_CHOICES)
	other_livestock_category = models.CharField(max_length=50, blank=True, null=True)
	number_of_animals_affected = models.IntegerField()
	sex_of_animals_affected = models.CharField(max_length=10, choices=SEX_CHOICES)
	age_of_animals_affected = models.CharField(max_length=10, choices=AGE_CHOICES)
	clinical_signs = models.TextField()
	number_of_dead_animals = models.IntegerField()
	propose_control_measures = models.TextField()
	sample_taken_to_lab = models.CharField(max_length=3, choices=YES_NO_CHOICES)
	tentative_diagnosis = models.TextField()
	village_disease_occurred = models.CharField(max_length=100)
	sub_county = models.CharField(max_length=100)
	county = models.CharField(max_length=100)
	owner_name = models.CharField(max_length=100)
	owner_mobile_number = models.CharField(max_length=20) 
	vet_in_charge_name = models.CharField(max_length=100)
	vet_registration_number = models.CharField(max_length=50)
	vet_mobile_number = models.CharField(max_length=20)
	signature=models.TextField(blank=True,null=True)
	#stamp = models.TextField(blank=True, null=True)

	def __str__(self):
		return f"Disease Report by {self.owner_name} on {self.village_disease_occurred}"

class Slaughterhouse(models.Model):
	CATEGORY_CHOICES = [
		('small_scale', 'Small Scale'),
		('large_scale', 'Large Scale'),
		# Add other categories if needed
	]
	
	SL_STATUS=[
		('private','Private'),
		('municipal','Municipal')
	]
	user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	assigned_to_official = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slaughter_house', limit_choices_to={'is_official': True})
	name = models.CharField(max_length=255)
	county = models.CharField(max_length=255)
	sub_county = models.CharField(max_length=255)
	location = models.CharField(max_length=255)
	slaughterhouse_status=models.CharField(max_length=50, choices=SL_STATUS)
	slaughterhouse_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
	livestock_slaughtered = models.CharField(max_length=255)  # Number of livestock slaughtered
	number_of_employees = models.IntegerField()
	roller_mark_number = models.CharField(max_length=50)
	inspector_name = models.CharField(max_length=255)
	inspector_registration_number = models.CharField(max_length=100)
	inspector_employment_number = models.CharField(max_length=100)
	inspector_mobile_number = models.CharField(max_length=15)

	def __str__(self):
		return self.name

# Employee Model
class Employee(models.Model):
    POSITION_CHOICES = [
        ('flager', 'Flager'),
        ('cleaner', 'Cleaner'),
        ('supervisor', 'Supervisor'),
        ('security_officer', 'Security Officer'),
    ]
    
    ML_LICENSE_CHOICES=[
		('updated','Updated'),
		('not_updated','Not Updated'),
	]
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    slaughterhouse = models.CharField(max_length=60)
    name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    medical_license_status = models.CharField(max_length=50,choices=ML_LICENSE_CHOICES)  
    
    def __str__(self):
        return self.name

# Butcher Details Model
class Butcher(models.Model):
    TRANSPORT_CHOICES = [
        ('motorbike', 'Motorbike'),
        ('vehicle', 'Vehicle'),
    ]
    LICENSE_CHOICES=[
		('updated','Updated'),
		('not_updated','Not Updated'),
	]
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    medical_license_status = models.CharField(max_length=50,choices=LICENSE_CHOICES)  # True for Updated, False for Not Updated
    livestock_slaughtered = models.CharField(max_length=50)  # Number of livestock slaughtered
    meat_container_number = models.CharField(max_length=50)
    meat_carrier_number = models.CharField(max_length=50)
    means_of_transport = models.CharField(max_length=50, choices=TRANSPORT_CHOICES)
    
    def __str__(self):
        return self.name

class Invoice(models.Model):
	ASSIGN_TO_CHOICES = [
		('farmer', 'Farmer'),
		('company', 'Company'),
	]

	INVOICE_CATEGORY_CHOICES = [
		('Deworming', 'Deworming'),
		('Surgery', 'Surgery'),
		('AI', 'Artificial Insemination'),
		('Clinical', 'Clinical'),
		('Vaccination', 'Vaccination'),
		('Post Mortem', 'Post Mortem'),
		('Pregnancy Diagnosis', 'Pregnancy Diagnosis'),
		('Lab Charges', 'Lab Charges'),
		('Farm Consultation', 'Farm Consultation'),
		('Visit', 'Visit'),
	]
	user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)	
	assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoice_report', limit_choices_to={'is_farmer': True})
	invoice_category = models.CharField(max_length=50, choices=INVOICE_CATEGORY_CHOICES)
	date_of_invoice = models.DateField()
	total_amount_due = models.DecimalField(max_digits=10, decimal_places=2)
	farmer_name = models.CharField(max_length=100)
	village = models.CharField(max_length=100)
	contact = models.CharField(max_length=15)
	vet_in_charge_of_invoice = models.CharField(max_length=100)
	vet_registration_number = models.CharField(max_length=100)
	vet_contact = models.CharField(max_length=15)
	signature = models.CharField(max_length=100, blank=True, null=True)
	stamp = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return f"Invoice {self.id} - {self.farmer_name}"

class DailyKill(models.Model):
	LIVESTOCK_CATEGORY_CHOICES = [
		('Cattle', 'Cattle'),
		('Sheep', 'Sheep'),
		('Goat', 'Goat'),
		('Pig', 'Pig'),
		# Add more categories as needed
	]

	CONDEMNATION_STATUS_CHOICES = [
		('Local Condemnation', 'Local Condemnation'),
		('Carcass Condemnation', 'Carcass Condemnation'),
	]

	INSPECTOR_STATUS_CHOICES = [
		('Employed', 'Employed'),
		('Delegated', 'Delegated'),
		('Intern/Student', 'Intern/Student'),
	]
	user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)	
	assigned_to_official = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  
        related_name='kills_official',
        limit_choices_to={'is_official': False},
        null=True,                 
        blank=True,
        editable=True,               
        default=1                  
    )
	date = models.DateField()
	livestock_category = models.CharField(max_length=50, choices=LIVESTOCK_CATEGORY_CHOICES)
	number_of_females_killed = models.PositiveIntegerField()
	number_of_males_killed = models.PositiveIntegerField()
	total_kills_per_day = models.PositiveIntegerField()
	condemnation_done = models.BooleanField(default=False)
	condemnation_status = models.CharField(max_length=50, choices=CONDEMNATION_STATUS_CHOICES, blank=True, null=True)
	comment_by_inspector = models.TextField(blank=True, null=True)
	inspector_name = models.CharField(max_length=100)
	inspector_reg_number = models.CharField(max_length=50)
	inspector_status = models.CharField(max_length=50, choices=INSPECTOR_STATUS_CHOICES)

	def __str__(self):
		return f"Daily Kill Record for {self.date} - {self.livestock_category}"

    
class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choice', on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

# class UserAnswer(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,default=1) 
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.user} - {self.question.text}"
    
    #tuutorials
    
class Tutorial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    lesson = models.CharField(max_length=255)
    cpd_number = models.CharField(max_length=30)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    points = models.IntegerField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lesson
class Section(models.Model):
    lesson = models.ForeignKey(Tutorial, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    file = models.FileField(upload_to='uploads/')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lesson.lesson} - {self.title}"
    
class Comment(models.Model):
    section = models.ForeignKey(Section, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.section.title}"

class CpdQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text


class CpdChoices(models.Model):
    question = models.ForeignKey(CpdQuestions, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.choice_text} - {'Correct' if self.is_correct else 'Incorrect'}"

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="results")
    score = models.FloatField()
    passed = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {'Pass' if self.passed else 'Fail'} - {self.score}%"
    

    
# class UserAnswers(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.user.username} - {self.question.text} - {self.choice.text}"
    
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.section.title} - Score: {self.score}"
    
class LivestockExaminationRecord(models.Model):
	LIVESTOCK_CATEGORIES = [
		('Cattle', 'Cattle'),
		('Sheep', 'Sheep'),
		('Goat', 'Goat'),
		('Poultry', 'Poultry'),
		('None', 'None'),
	]

	REASONS_FOR_EXAMINATION = [
		('Slaughter', 'Slaughter'),
		('Breeding', 'Breeding'),
		('Culling', 'Culling'),
		('Disease Control', 'Disease Control'),
		('For Sale', 'For Sale'),
	]
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	assigned_to_official = models.ForeignKey(User, on_delete=models.CASCADE, related_name='examination_report', limit_choices_to={'is_official': True})
	livestock_category = models.CharField(max_length=50, choices=LIVESTOCK_CATEGORIES)
	other_category = models.CharField(max_length=100, blank=True, null=True)
	age_of_animal = models.PositiveIntegerField()
	breed = models.CharField(max_length=100)
	sex_of_animal = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
	number_of_animals = models.PositiveIntegerField()
	origin_of_animal = models.CharField(max_length=100)
	destination = models.CharField(max_length=100)
	reason_for_examination = models.CharField(max_length=50, choices=REASONS_FOR_EXAMINATION)
	recommendation = models.TextField()
	owner_name = models.CharField(max_length=100)
	owner_mobile_number = models.CharField(max_length=15)
	veterinary_officer_in_charge = models.CharField(max_length=100)
	registration_number = models.CharField(max_length=50)
	veterinary_officer_mobile_number = models.CharField(max_length=15)
	veterinary_officer_signature = models.TextField()

	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.livestock_category} Examination Record - {self.owner_name}"
class CalvingRecord(models.Model):
	CALVING_PROCEDURES = [
		('Normal', 'Normal'),
		('Assisted', 'Assisted'),
		('C-Section', 'C-Section'),
	]

	RAB_STATUSES = [
		('Natural Expulsion', 'Natural Expulsion'),
		('Manual Removal', 'Manual Removal'),
	]

	CALF_STATUS = [
		('Live', 'Live'),
		('Dead', 'Dead'),
	]

	REASONS_FOR_DEAD_FOETUS = [
		('Delayed Labour', 'Delayed Labour'),
		('Breech Presentation', 'Breech Presentation'),
		('None', 'None'),
	]
	user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)	
	assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calving_report', limit_choices_to={'is_farmer': True})
	date_of_calving = models.DateField()
	insemination_date = models.DateField(blank=True, null=True)
	days_to_calving_down = models.PositiveIntegerField(help_text="Number of days to calving down")
	cow_name = models.CharField(max_length=100)
	registration_number = models.CharField(max_length=50, blank=True, null=True)
	calving_procedure = models.CharField(max_length=20, choices=CALVING_PROCEDURES)
	rab_status = models.CharField(max_length=20, choices=RAB_STATUSES)
	hours_for_natural_expulsion = models.PositiveIntegerField()
	calf_sex = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')])
	calf_status = models.CharField(max_length=10, choices=CALF_STATUS)
	reason_for_dead_foetus = models.CharField(max_length=50, choices=REASONS_FOR_DEAD_FOETUS, blank=True, null=True)
	comment = models.TextField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Calving Record for {self.cow_name} - {self.date_of_calving}"

class AssessmentRecord(models.Model):
	LIVESTOCK_CATEGORIES = [
		('Cattle', 'Cattle'),
		('Sheep', 'Sheep'),
		('Goat', 'Goat'),
		('Dog', 'Dog'),
		('Cat', 'Cat'),
		('Horse', 'Horse'),
		('None', 'None'),
	]

	SEX_CHOICES = [
		('Male', 'Male'),
		('Female', 'Female'),
	]

	PLACE_OF_ASSESSMENT_CHOICES = [
		('Farm', 'Farm'),
		('Market', 'Market'),
	]

	REASON_FOR_ASSESSMENT_CHOICES = [
		('Slaughter', 'Slaughter'),
		('Breeding', 'Breeding'),
		('Culling', 'Culling'),
		('Disease Control', 'Disease Control'),
		('Sales', 'Sales'),
		('For Complaint', 'For Complaint'),
		('Theft Cases', 'Theft Cases'),
		('For Export', 'For Export'),
	]
	user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)	
	assigned_to_official = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assesment_report', limit_choices_to={'is_farmer': True})
	livestock_category = models.CharField(max_length=20, choices=LIVESTOCK_CATEGORIES)
	other_category = models.CharField(max_length=50, blank=True, null=True)
	date_of_assessment = models.DateField()
	name_of_animal = models.CharField(max_length=100)
	registration_number = models.CharField(max_length=50)
	color_of_animal = models.CharField(max_length=50)
	age_of_animal = models.PositiveIntegerField()  # Assuming age is in years
	sex_of_animal = models.CharField(max_length=10, choices=SEX_CHOICES)
	number_of_animals = models.PositiveIntegerField()
	origin_of_animal = models.CharField(max_length=100)
	place_of_assessment = models.CharField(max_length=20, choices=PLACE_OF_ASSESSMENT_CHOICES)
	destination = models.CharField(max_length=100)
	reason_for_assessment = models.CharField(max_length=50, choices=REASON_FOR_ASSESSMENT_CHOICES)
	recommendation = models.TextField(blank=True, null=True)
	owner_of_animal = models.CharField(max_length=100)
	owner_mobile_number = models.CharField(max_length=15)
	veterinary_practitioner_in_charge = models.CharField(max_length=100)
	practitioner_registration_number = models.CharField(max_length=50)
	practitioner_contact = models.CharField(max_length=15)
	signature_and_stamp = models.CharField(max_length=100)  # Assuming signature and stamp will be an image

	def __str__(self):
		return f"{self.livestock_category} - {self.name_of_animal} ({self.date_of_assessment})"

class MovementPermit(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)	
	assigned_to_official = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movement_permit', limit_choices_to={'is_official': True}, default=1)
	date_of_permit = models.DateField()
	sub_county_district = models.CharField(max_length=100)
	ward_level = models.CharField(max_length=100)
	authorized_by = models.CharField(max_length=100)
	registration_number = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=15)
	uploaded_permit = models.FileField(upload_to='movement_permits/')

	def __str__(self):
		return f"Permit {self.registration_number} - {self.date_of_permit}"

class NoObjection(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)	
	assigned_to_official = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noobjection_form', limit_choices_to={'is_official': True}, default=1)
	date_of_confirmation = models.DateField()
	sub_county_district = models.CharField(max_length=100)
	ward_level = models.CharField(max_length=100)
	confirmed_by = models.CharField(max_length=100)
	registration_number = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=15)
	uploaded_no_objection_form = models.FileField(upload_to='no_objection_forms/')

	def __str__(self):
		return f"No Objection {self.registration_number} - {self.date_of_confirmation}"
class MonthlyReport(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)	
	assigned_to_official = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  
        related_name='monthly_reports_official',
        limit_choices_to={'is_official': True},
        null=True,                 
        blank=True,               
        default=1                  
    )
	date_of_submission = models.DateField()
	sub_county = models.CharField(max_length=100)
	ward_level = models.CharField(max_length=100)
	submitted_by = models.CharField(max_length=100)
	registration_number = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=15)
	uploaded_report = models.FileField(upload_to='monthly_reports/')

	def __str__(self):
		return f"Monthly Report - {self.date_of_submission} by {self.submitted_by}"

class QuarterlyReport(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)	
	assigned_to_official = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  
        related_name='quartely_reports_official',
        limit_choices_to={'is_official': True},
        null=True,                 
        blank=True,               
        default=1                  
    )
	date_of_submission = models.DateField()
	sub_county = models.CharField(max_length=100)
	ward_level = models.CharField(max_length=100)
	submitted_by = models.CharField(max_length=100)
	registration_number = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=15)
	uploaded_report = models.FileField(upload_to='monthly_reports/')

	def __str__(self):
		return f"Monthly Report - {self.date_of_submission} by {self.submitted_by}"
class YearlyReport(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)	
	assigned_to_official = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  
        related_name='yearly_reports_official',
        limit_choices_to={'is_official': True},
        null=True,                 
        blank=True,               
        default=1                  
    )
	date_of_submission = models.DateField()
	sub_county = models.CharField(max_length=100)
	ward_level = models.CharField(max_length=100)
	submitted_by = models.CharField(max_length=100)
	registration_number = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=15)
	uploaded_report = models.FileField(upload_to='monthly_reports/')

	def __str__(self):
		return f"Monthly Report - {self.date_of_submission} by {self.submitted_by}"



class Practitioner(models.Model):
	SPECIALIZATION_CHOICES = [
		('large_animals', 'Large Animals'),
		('small_animals', 'Small Animals'),
	]

	VET_CATEGORY_CHOICES = [
		('surgeon', 'Surgeon'),
		('technologist', 'Technologist'),
		('technician', 'Technician'),
	]
 
	EMP_STATUS_CHOICES=[
		('employed','Employed'),
		('private_practitioner','Private Practitioneer ')
	]





	user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
	assigned_to_official = models.ForeignKey(
		User, on_delete=models.CASCADE, related_name='practitioner_record',
		limit_choices_to={'is_official': True}, default=1
	)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	reg_date=models.DateField()
	phone_number = models.CharField(max_length=20)
	email = models.CharField(max_length=100)
	county = models.CharField(max_length=30)
	subcounty = models.CharField(max_length=30)
	ward = models.CharField(max_length=30)
	area_of_operation = models.CharField(max_length=30)
	specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
	vet_category = models.CharField(max_length=50, choices=VET_CATEGORY_CHOICES)
	registration_number = models.CharField(max_length=50)
	employment_status=models.CharField(max_length=50,choices=EMP_STATUS_CHOICES)

	def __str__(self):
		return f"{self.first_name} {self.last_name} - {self.specialization}"