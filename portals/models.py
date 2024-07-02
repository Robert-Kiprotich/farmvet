from django.db import models
from django.contrib.auth.models import User
from user.models import *


SPECIES_CHOICES = (
    ('0', 'cattle'),
    ('1', 'sheep'),
	('2', 'goat'),
	('3', 'donkey'),
	('4', 'dog'),
	('5', 'horse'),
	('6', 'poultry'),
	('7','others')
)

DISEASE_CHOICES = (
	('A','acute'),
	('S','sub_acute')

)

BREEDING_LEVEL_CHOICES = [
		('Purebred', 'Purebred'),
		('Crossbred', 'Crossbred'),
		('MixedBreed', 'MixedBreed'),
	]

DIAGNOSIS_CHOICES = (
	('C','clinical_signs'),
	('L','laboratory')
)

PROGNOSIS_CHOICES=(
	('G','good'),
	('F','fair'),
	('P','poor')
)


YES_NO_CHOICES = (
	('Y','yes'),
	('N','no')
)


OPERATION_CHOICES=(
	('C','c_section'),
 	('I','interstinal_torsion'),
 	('T','tumor_extraction'),
 	('C','canine_spaying'),
 	('H','hernia'),
 	('W','Warts_extraction'),
 	('C','castration'),
 	('S','skin_injuries'),
 	('F','fructure'),
	('R','rumenatomy'),
 	('O','other'),
)

VACCINATION_CHOICES=(
	('M','Mass_vaccination'),
 	('R','Ring_vaccination'),
 	('I','Individual')
)

SEX_CHOICES = (
 	('Male','Male'),
 	('Female','Female')
 )


NATURE_CHOICES=(
 	('A','Alive'),
 	('D','Dead')
 )

FARM_MANAGER = (
	('V', 'Veterinary Officer'),
	('L', 'Livestock Officer'),
	('N', 'None')
)

COW_CATEGORY=(
	('A','Adult'),
	('H','Heifer')
)


STATUS_CHOICES=(
 	('H','Healthy'),
 	('D','Deformed')
 )

BREECHING_LEVEL=(
 	('F','First'),
 	('S','Second'),
 	('T','Third'),
 	('P','Pedegree')
)

RESULT_CHOICES=(
 	('P','positive'),
 	('N','Negative')
)

PAYMENT=(
	('F','Full'),
	('I','Instalments')
)


#farmers = [farmer.user.first_name + ' ' +farmer.user.last_name for farmer in Farmer.objects.all()]

farmers_list = []

#key = 1

# for farmer in farmers:
#     farmer_tuple = (farmer, farmer)
#     #key+=1
#     farmers_list.append(farmer_tuple)
    
    

FARMERS = tuple(farmers_list)



class Vet_Forms(models.Model):
	vet_username = models.CharField(max_length=20)
	is_sick_approach_form = models.BooleanField(default=False)
	is_dead_approach_form= models.BooleanField(default=False)
	is_surgical_approach_form = models.BooleanField(default=False)
	is_deworming_form = models.BooleanField(default=False)
	is_vaccination_form = models.BooleanField(default=False)
	is_artificial_insemination_form = models.BooleanField(default=False)
	is_calf_registration_form = models.BooleanField(default=False)
	is_livestock_inventory_form = models.BooleanField(default=False)
	is_farm_consultation = models.BooleanField(default=False)
	is_pregnancy_diagnosis_form = models.BooleanField(default=False)
	is_vet_billing_form = models.BooleanField(default=False)
	is_lab_form = models.BooleanField(default=False)
	is_referral_form = models.BooleanField(default=False)
	report_created_on = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-report_created_on']

	def __str__(self):
		return self.vet_username	


class Sick_Approach_Form(models.Model):
	vet_form = models.OneToOneField(Vet_Forms, on_delete=models.CASCADE, primary_key=True)
	# farmer_username = models.CharField(max_length=100, choices=FARMERS, verbose_name='Farmer Username')
	farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
	species_affected = models.CharField(max_length=20, choices=SPECIES_CHOICES, default='0', verbose_name='animal species affected',null=True, blank=True)
	num_of_species_affected = models.PositiveIntegerField(verbose_name='number of species affected' ,null=True, blank=True)
	id_animal = models.CharField(max_length=100, verbose_name='name of the animal/identification number', null=True, blank=True)
	disease_nature = models.CharField(max_length=20, choices=DISEASE_CHOICES, default='0', verbose_name='nature of the disease' ,null=True, blank=True)
	clinical_signs = models.CharField(max_length=100)
	disease_diagnosis = models.CharField(max_length=20, choices=DIAGNOSIS_CHOICES, default='0' ,null=True, blank=True)
	differential_diagnosis = models.CharField(max_length=100, null=True, blank=True)
	final_diagnosis = models.CharField(max_length=100 ,null=True, blank=True)
	sickness_duration = models.CharField(max_length=100, verbose_name='duration of the sickness' ,null=True, blank=True)
	sickness_history = models.CharField(max_length=300, null=True, blank=True)
	drug_of_choice = models.CharField(max_length=100, null=True, blank=True)
	treatment_duration = models.CharField(max_length=100 ,null=True, blank=True) 
	start_dose_date = models.DateField()
	prognosis = models.CharField(max_length=20, choices=PROGNOSIS_CHOICES, default='G' ,null=True, blank=True)
	harmony_with_clinic_signs_and_lab = models.CharField(max_length=5, choices=YES_NO_CHOICES, default='Y',verbose_name='were the pathological signs in harmony with the clinical signs and laboratory reports?' ,null=True, blank=True)
	cause_of_death_if_in_no_harmony = models.CharField(max_length=100, null=True, blank=True,verbose_name='If no, what could be the cause of the death')
	disease_one_of_the_zoonotic = models.CharField(max_length=5, choices=YES_NO_CHOICES, default='0', verbose_name='is the disease one of the zoonotic?' ,null=True, blank=True)
	advice_given_if_zoonotic = models.CharField(max_length=100, null=True, blank=True, verbose_name='if yes, what advice did you give the owner and people who handled the carcass')
	relapse = models.CharField(max_length=5, choices=YES_NO_CHOICES, default='0', verbose_name='was there any relapse?')
	cause_if_relapse = models.CharField(max_length=100, null=True, blank=True, verbose_name='if yes, what might be the cause')
	comment = models.CharField(max_length=300,null=True,blank=True,verbose_name='comment')
	
	def __str__(self):
		return f'Sick Form for farmer - {self.farmer}'
	

class Death_Approach_Form(models.Model):
	vet_form = models.OneToOneField(Vet_Forms, on_delete=models.CASCADE, primary_key=True)
	farmer_username = models.CharField(max_length=12,verbose_name='Farmer Username')
	name_of_the_animal = models.CharField(max_length=30,null=True,blank=True,verbose_name='Name or identification number')
	sex_of_the_animal = models.CharField(max_length=20,choices=SEX_CHOICES,default='',verbose_name='Sex of the animal' ,null=True, blank=True)
	num_of_species_dead = models.IntegerField(default=1,null=True, blank=True,verbose_name='Number of animals dead')
	case_history = models.CharField(max_length=100, default='' ,null=True, blank=True)
	mortality_rate = models.CharField(max_length=100, default='' ,null=True, blank=True)
	death_date = models.DateField(verbose_name='Date the animal died' ,null=True, blank=True)
	death_time = models.TimeField(verbose_name='At what time the animal the animals died' ,null=True, blank=True)
	signs_of_cadever_on_the_ground = models.CharField(max_length=200,verbose_name='What are the signs of signs of the cadever on the ground' ,null=True, blank=True)
	carcass_opened_for_the_pm = models.CharField(max_length=5, choices=YES_NO_CHOICES,default='Y',verbose_name='Did you open up the carcass fo PM?' ,null=True, blank=True)
	if_yes_pathological_signs = models.CharField(max_length=100, null=True, blank=True,verbose_name='If yes,what were the signs of the pathological conditions?')
	if_no_reason = models.CharField(max_length=100, null=True, blank=True,verbose_name='If no,what could have been the reason?')
	sample_sent_lab = models.CharField(max_length=5, choices=YES_NO_CHOICES, default='Y',null=True,verbose_name='Did you send any sample to the laboratory?')
	if_yes_lab_report = models.CharField(max_length=100, null=True, blank=True,verbose_name='if yes,what was the laboratory report?')
	death_cause_notifiable = models.CharField(max_length=5, choices=YES_NO_CHOICES, default='Y',verbose_name='Is the cause of dead notifiable?' ,null=True, blank=True)
	if_yes_message_to_relevant_body = models.CharField(max_length=100, null=True, blank=True,verbose_name='If yes,send message to the relevant body.')
	intervention_regards_to_death = models.CharField(max_length=100, null=True, blank=True,verbose_name='What were the necessary intervention in regard to the cause of the dead')
	comment = models.CharField(max_length=300,null=True,blank=True,verbose_name='comment')

	def __str__(self):
		return f'Name of form: Death Approach Form'


class Surgical_Approach_Form(models.Model):
	vet_form = models.OneToOneField(Vet_Forms, on_delete=models.CASCADE, primary_key=True)
	farmer_username = models.CharField(max_length=12,verbose_name='Farmer Username', default='')
	species_operated_on = models.CharField(max_length=20, choices=SPECIES_CHOICES, default='0',verbose_name='Animal species affected' ,null=True, blank=True)
	if_other_specify = models.CharField(max_length=100, null=True, blank=True,verbose_name='If,other specify.')
	sex_of_the_animal = models.CharField(max_length=20,choices=SEX_CHOICES, default='', verbose_name='Sex of the animal' ,null=True, blank=True)
	name_of_the_animal = models.CharField(max_length=30,null=True,blank=True,verbose_name='Name or identification number')
	operation_nature= models.CharField(max_length=20, choices=OPERATION_CHOICES,default='C', verbose_name='Nature of operation' ,null=True, blank=True)
	if_other_specify = models.CharField(max_length=100, null=True, blank=True)
	operation_date = models.DateField(verbose_name='Date of Operation',null=True, blank=True)
	post_operation_management = models.CharField(max_length=100, default='',null=True, blank=True, verbose_name='Post operation management')
	prognosis = models.CharField(max_length=100, default='',null=True, blank=True,verbose_name='Prognosis')
	comment = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return f'Name of form: Surgical Approach Form'


class Deworming_Form(models.Model):
	vet_form = models.OneToOneField(Vet_Forms, on_delete=models.CASCADE, primary_key=True)
	farmer_username = models.CharField(max_length=12,verbose_name='Farmer Username')
	species_targeted = models.CharField(max_length=20, choices=SPECIES_CHOICES, default='0',verbose_name='Species targetted' ,null=True, blank=True)
	number_of_adults = models.PositiveIntegerField(default=0,null=True, blank=True,verbose_name='Number of adults')
	number_of_young_ones = models.PositiveIntegerField(default=0,null=True, blank=True,verbose_name='Number of young ones')
	body_condition_of_the_animal = models.CharField(max_length=20, choices=PROGNOSIS_CHOICES, default='G',verbose_name='Body condition of the animal(s)' ,null=True, blank=True)
	date_of_deworming = models.DateField()
	drug_choices = models.CharField(max_length=100, default='',verbose_name='Drug of choice' ,null=True, blank=True)
	target_parasites = models.CharField(max_length=100, null=True, blank=True,verbose_name='Target parasite')
	withdrawal_period = models.CharField(max_length=100 ,null=True, blank=True)
	side_effects = models.CharField(max_length=100, null=True, blank=True,verbose_name='Any side effect?')
	next_date_deworming = models.DateField(verbose_name='Next date of deworming')
	comment = models.CharField(max_length=100, null=True, blank=True)

	
	def __str__(self):
		return f'Name of form: Deworming Approach Form'


class Vaccination_Form(models.Model):
	vet_form = models.OneToOneField(Vet_Forms, on_delete=models.CASCADE, primary_key=True)
	farmer_username = models.CharField(max_length=12,verbose_name='Farmer Username')
	species_targeted = models.CharField(max_length=20, choices=SPECIES_CHOICES, default='0',verbose_name='Animal species targetted')
	if_other_specify = models.CharField(max_length=100, null=True, blank=True,verbose_name='If other specify')
	number_of_animals_vaccinated= models.IntegerField(default=1,null=True,blank=True,verbose_name='Number of animals vaccinated.')
	age_of_animal = models.PositiveIntegerField(default=1,null=True,blank=True,verbose_name='Age of animal')
	sex_of_the_animal = models.CharField(max_length=20,choices=SEX_CHOICES,default='M', verbose_name='Sex of the animal' ,null=True, blank=True)
	animal_breed = models.CharField(max_length=100, null=True, blank=True,verbose_name='Breed of the animal')
	animal_colour = models.CharField(max_length=100,null=True,verbose_name='Colour of the animal')
	other_description = models.CharField(max_length=100,null=True,blank=True,verbose_name='other description')
	targetted_disease = models.CharField(max_length=20,null=True,verbose_name='The disease target')
	vaccines_used = models.CharField(max_length=100, null=True, blank=True,verbose_name='Vaccine used')
	date_of_vaccination = models.DateField(verbose_name='Date of vaccination')
	next_date_of_vaccination = models.DateField(verbose_name='Next date of vaccination')
	name_of_the_crush = models.CharField(max_length=100, null=True, blank=True,verbose_name='Name of the crush')
	nature_of_the_vacination_program = models.CharField(max_length=200, choices=VACCINATION_CHOICES, default='M',verbose_name='Nature of the vaccination program')
	comment = models.CharField(max_length=100, null=True, blank=True)

	
	def __str__(self):
		return f'Name of form: Vaccination Approach Form'


class Artificial_Insemination_Form(models.Model):
	vet_form = models.OneToOneField(Vet_Forms, on_delete=models.CASCADE, primary_key=True)
	farmer_username = models.CharField(max_length=12,verbose_name='Farmer Username')
	Name_of_the_cow = models.CharField(max_length=12,verbose_name='Name of the cow or identification number of the cow')
	sex_of_the_calf_born = models.CharField(max_length=20, choices=SEX_CHOICES, default='M',verbose_name='Sex of the calf born')
	date_of_birth = models.DateField(verbose_name='Date of birth')
	nature_of_birth = models.CharField(max_length=20, choices=NATURE_CHOICES, default='A',verbose_name='Nature of birth')
	number_of_repeat = models.CharField(max_length=100, null=True, blank=True,verbose_name='Number of repeat')
	abortion_rate = models.CharField(max_length=100, null=True, blank=True,verbose_name='Abortion rate')
	reason_for_the_cause_of_abortion = models.CharField(max_length=100, null=True, blank=True,verbose_name='reason for abortion')
	time_of_heat_sign = models.TimeField(verbose_name='Time of heat sign')
	date_of_insemination = models.DateField(verbose_name='Date of insemination')
	time_of_insemination = models.TimeField(verbose_name='Time of insemination')
	nature_of_the_breeding = models.CharField(max_length=100, null=True, blank=True,verbose_name='Nature of breeding')
	sire_name = models.CharField(max_length=200,null=True,blank=True,verbose_name='Sire`s name')
	sire_origin = models.CharField(max_length=200,null=True,blank=True,verbose_name='Sire origin')
	bull_code= models.CharField(max_length=100, null=True, blank=True,verbose_name='Bull code')
	breed_used = models.CharField(max_length=100, null=True, blank=True,verbose_name='Breed used')
	source_of_semen = models.CharField(max_length=100, null=True, blank=True,verbose_name='Source of the semen')
	date_of_repeat_checked = models.DateField(verbose_name='Date of repeat check')
	date_of_pregnancy_diagnosis = models.DateField(verbose_name='Date of pregnancy')
	expected_date_of_calving = models.DateField(verbose_name='expected date of calving')
	comment = models.CharField(max_length=100, null=True, blank=True)

	
	def __str__(self):
		return f'Name of form: Artificial Approach Form'


class Calf_Registration_Form(models.Model):
	vet_form = models.OneToOneField(Vet_Forms, on_delete=models.CASCADE, primary_key=True)
	farmer_username = models.CharField(max_length=12,verbose_name='Farmer Username', default='')
	date_of_birth = models.DateField(verbose_name='Date of birth')
	sex_of_the_calf = models.CharField(max_length=20, choices=SEX_CHOICES, default='M',verbose_name='Sex of the calf')
	birth_weight = models.IntegerField(verbose_name='Birth weight')
	breed_of_the_calf = models.CharField(max_length=20,verbose_name='breed of the calf')
	colour_of_the_breed= models.CharField(max_length=20,verbose_name='Colour of the breed')
	status_of_the_calf = models.CharField(max_length=100, choices=STATUS_CHOICES, default='H',verbose_name='Status of the calf')
	breeching_level_of_the_calf = models.CharField(max_length=100, choices=BREECHING_LEVEL, default='F',verbose_name='Breeching level of the calf')
	sire_details = models.CharField(max_length=100, null=True, blank=True)
	expected_date_of_weaning = models.DateField(verbose_name='Expected date of weaning')
	comment = models.CharField(max_length=100, null=True, blank=True)

	
	def __str__(self):
		return f'Name of form: Calf Registration Approach Form'


class Livestock_Inventory_Form(models.Model):
	vet_form = models.OneToOneField(Vet_Forms, on_delete=models.CASCADE, primary_key=True)
	farmer_username = models.CharField(max_length=12,verbose_name='Farmer Username')
	species_targeted = models.CharField(max_length=20, choices=SPECIES_CHOICES, default='0',verbose_name='Species targetted')
	name_of_the_animal = models.CharField(max_length=30,null=True,blank=True,verbose_name='Name or identification number')
	number_of_the_male_animals= models.IntegerField(default=1,null=True,blank=True,verbose_name='Number of male animals')
	number_of_the_female_animals= models.IntegerField(default=1,null=True,blank=True,verbose_name='Number of female animals')
	number_of_live_animals= models.IntegerField(default=1,null=True,blank=True,verbose_name='Number of live animals')
	number_of_dead_animals= models.IntegerField(default=1,null=True,blank=True,verbose_name='Number of dead animals')
	specify_the_cause_of_the_dead = models.CharField(max_length=100, null=True, blank=True,verbose_name='Specify the cause of dead')
	is_your_animals_insured = models.CharField(max_length=20, choices=YES_NO_CHOICES, default='Y',verbose_name='Has your animals been insured?')
	if_yes_give_insuring_company = models.CharField(max_length=100, null=True, blank=True,verbose_name='If yes,give the insuring company')
	date_of_culling = models.DateField(verbose_name='Date of culling')
	give_reason_for_culling = models.CharField(max_length=200,null=True,blank=True,verbose_name='Give reason for culling')
	#Attach_photos_of_your_animal = models.ImageField(upload_to='vet_photos', height_field=None, width_field=None, default='default.jpg', max_length=100,verbose_name='Upload photos')
	comment = models.CharField(max_length=100, null=True, blank=True)
	

	def __str__(self):
		return self.name + ' - ' + str(self.id)


class Pregnancy_Diagnosis_Form(models.Model):
	vet_form = models.OneToOneField(Vet_Forms, on_delete=models.CASCADE, primary_key=True)
	farmer_username = models.CharField(max_length=12,verbose_name='Farmer Username')
	cow_name = models.CharField(max_length=20,null=True,blank=True,verbose_name='Name or idenfication number of the cow')
	cow_category = models.CharField(max_length=50,choices = COW_CATEGORY,default='H', verbose_name='Cow`s category')
	date_of_insemination = models.DateField(verbose_name='Date of insemination')
	date_of_pregnancy_diagnosis = models.DateField(verbose_name='date of pregnancy diagnosis')
	result_of_diagnosis = models.CharField(max_length=20, choices = RESULT_CHOICES, verbose_name='Results of diagnosis')
	if_positive = models.CharField(max_length=100,null=True,blank=True,verbose_name='If the result is positive give the approximate age of the fetus.')
	if_result_is_negative_give_observation = models.CharField(max_length=100, null=True, blank=True,verbose_name='If the result test negative give your observation')
	next_date_of_pregnancy_diagnosis = models.DateField(verbose_name='Next date of pregnancy diagnosis')
	expected_date_of_delivery = models.DateField(verbose_name='Expected date of delivery')
	comment = models.CharField(max_length=100, null=True, blank=True,verbose_name='Comment')

	def __str__(self):
		return f'Name of form: Pregnancy Diagnosis Form'

class Farm_Consultation(models.Model):
	vet_form = models.OneToOneField(Vet_Forms, on_delete=models.CASCADE, primary_key=True)
	farmer_username = models.CharField(max_length=12,verbose_name='Farmer Username')
	dairy_cows = models.CharField(max_length=12,null=True,blank=True,verbose_name='Dairy cows unit')
	beef_production = models.CharField(max_length=20,null=True,blank=True,verbose_name='Beef production unit')
	poultry = models.CharField(max_length=30,null=True,blank=True,verbose_name='Poultry production unit')
	sheep = models.CharField(max_length=50,null=True,blank=True,verbose_name='Sheep production unit')
	goat = models.CharField(max_length=100,null=True,blank=True,verbose_name='Goat production unit')
	canine = models.CharField(max_length=100,null=True,blank=True,verbose_name='Canine keeping')
	other = models.CharField(max_length=100,null=True,blank=True,verbose_name='Other livestock')
	give_recommendation = models.CharField(max_length=100,null=True,blank=True,verbose_name='Give recommendation.')
	grazing = models.CharField(max_length=200, null=True, blank=True, verbose_name='Grazing system and pasture management.')
	disease = models.CharField(max_length=100, null=True, blank=True,verbose_name='Disease control.')
	farm = models.CharField(max_length=100, null=True, blank=True, verbose_name='Farm biosecurity')
	culling_selection = models.CharField(max_length=100, null=True,blank=True, verbose_name='Culling and Selection.')
	farm_manager = models.CharField(max_length=20, choices=FARM_MANAGER, default='',verbose_name='Is the farm managed by a veterinary officer or livestock officer?')
	if_no = models.CharField(max_length=100, null=True,blank=True, verbose_name='If none,who is the farm consultant?')
	name_incharge = models.CharField(max_length=100, null=True, blank=True,verbose_name='Name of the veterinary officer incharge.')
	reg_number = models.CharField(max_length=100, null=True, blank=True,verbose_name='Registration number.')
	comment = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return f'Name of form: farm consultation'

class Veterinary_Billing_Form(models.Model):
	vet_form = models.OneToOneField(Vet_Forms, on_delete=models.CASCADE, primary_key=True)
	farmer_username = models.CharField(max_length=12,verbose_name='Farmer Username')
	Mobile_number = models.IntegerField(default=1,null=True,blank=True,verbose_name='Mobile number of the farmer')
	farmer_location = models.CharField(max_length=100, null=True, blank=True,verbose_name='Location of the farmer.')
	nature_of_problem = models.CharField(max_length=100, null=True, blank=True,verbose_name='Nature of problem bill is done for.')
	bill_paid = models.CharField(max_length=100, null=True, blank=True,verbose_name='Total amount billed.')
	total_bill = models.CharField(max_length=100, null=True, blank=True,verbose_name='Total bill paid by the farmer.')
	balance_due = models.CharField(max_length=100, null=True, blank=True,verbose_name='Balance due to be paid.')
	agreed_date =  models.DateField(max_length=100, null=True, blank=True,verbose_name='Agreed date of payment.')
	suggest_payment = models.CharField(max_length=20, choices=PAYMENT, default='0', verbose_name='Suggest payment plan for the balance',null=True, blank=True)
	vet_name =  models.CharField(max_length=12,verbose_name='Veterinary officer claiming the bill.')
	registration_number = models.CharField(max_length=100, verbose_name='Registration number', null=True, blank=True)
	Mobile_number = models.IntegerField(null=True,blank=True,verbose_name='Mobile number')
	comment = models.CharField(max_length=100, null=True, blank=True)


	def __str__(self):
		return f'Name of form: Veterinary Billing Form'

class Laboratory_Form(models.Model):
	vet_form = models.OneToOneField(Vet_Forms, on_delete=models.CASCADE, primary_key=True)
	farmer_username = models.CharField(max_length=12,verbose_name='Farmer Username')
	Mobile_number = models.IntegerField(null=True,blank=True,verbose_name='Mobile number')
	category_ssp = models.CharField(max_length=12,verbose_name='Category of the spp')
	sample = models.CharField(max_length=12,verbose_name='Samples collected')
	name_animal = models.CharField(max_length=12,verbose_name='Namer of the animal')
	date_of_submission = models.DateField(verbose_name='Date of submission')
	idenfication = models.IntegerField(null=True,blank=True,verbose_name='ID number')
	storage = models.CharField(max_length=100,verbose_name='Method of storage')
	transportation =  models.CharField(max_length=200,verbose_name='Transportation means')
	expected_duration =  models.CharField(max_length=100,verbose_name='Expected duration of the sampling process')
	sample_collected_sick_animal = models.CharField(max_length=5, choices=YES_NO_CHOICES, default='Y',null=True,verbose_name='Was the sample collected for sick animal?')
	sample_collected_dead = models.CharField(max_length=5, choices=YES_NO_CHOICES, default='Y',null=True,verbose_name='Was the sample collected from a dead animal?')
	if_yes_sick = models.CharField(max_length=100, null=True, blank=True,verbose_name='If yes,state the signs shown by the cadaver')
	findings = models.CharField(max_length=100,verbose_name='What was the laboratory findings?')
	vet_name =  models.CharField(max_length=12,verbose_name='Name of the Veterinary officer who collected the sample.')
	registration_number = models.CharField(max_length=100, verbose_name='Registration number', null=True, blank=True)
	Mobile_number = models.IntegerField(null=True,blank=True,verbose_name='Mobile number')
	laboratory_offficer = models.CharField(max_length=20,verbose_name='Name of the laboratory officer')
	registration_number = models.CharField(max_length=100, verbose_name='Registration number', null=True, blank=True)
	Mobile_number = models.IntegerField(null=True,blank=True,verbose_name='Mobile number')
	comment = models.CharField(max_length=100, null=True, blank=True)




	def __str__(self):
		return f'Name of form: Laboratory Form'

class Referral_Form(models.Model):
	vet_form = models.OneToOneField(Vet_Forms, on_delete=models.CASCADE, primary_key=True)
	farmer_username = models.CharField(max_length=12,verbose_name='Farmer Username')
	Mobile_number = models.IntegerField(null=True,blank=True,verbose_name='Mobile number')
	case_referal = models.CharField(max_length=20, choices=YES_NO_CHOICES, default='Y' ,verbose_name='Is the case referal to another vet?')
	previous_treated = models.CharField(max_length=12,verbose_name='State the previous treated given')
	state_prognosis = models.CharField(max_length=100,verbose_name='state the prognosis of the animal on referal.')
	referal_date = models.DateField(verbose_name='referal date')
	suggest_vet = models.CharField(max_length=20, choices=YES_NO_CHOICES, default='Y' ,verbose_name='Do you suggest a vet to be referred to?')
	if_yes_leave_phone_number = models.CharField(max_length=100, null=True, blank=True,verbose_name='If yes,write phone number of the vet')
	registration_number = models.CharField(max_length=15, verbose_name='Registration number of the vet')
	comment = models.CharField(max_length=100, null=True, blank=True)
	def __str__(self):
		return f'Name of form: Referral Form'

class Calf(models.Model):
	
	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	name_given = models.CharField(max_length=100, default='')
	birth_date = models.DateField()
	breed = models.CharField(max_length=100, default='')
	gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='')
	sire_details = models.CharField(max_length=100, default='')
	color = models.CharField(max_length=100, default='')
	birth_weight = models.FloatField()
	medical_conditions = models.CharField(max_length=100, blank=True, default='')
	registration_number = models.CharField(max_length=100, unique=True, default='')
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
	age = models.CharField(max_length=100, default='')
	gender = models.CharField(max_length=100, default='')
	animal_type=models.CharField(max_length=100, choices=ANIMAL_TYPE, default='')
	breed = models.CharField(max_length=100, default='')
	culling_method = models.CharField(max_length=100, choices=CULLING_METHOD, default='')
	no_of_culled = models.FloatField(default=0)
	culling_reason = models.CharField(max_length=100, choices=CULLING_REASONS, default='')
	reg_no = models.CharField(max_length=100, unique=True, default='')
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
	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	name = models.CharField(max_length=100)
	reg_no = models.CharField(max_length=50)
	date_of_ai = models.DateField()
	exp_heat_date = models.DateField()
	first_preg_diag_date = models.DateField()
	PD_STATUS_CHOICES = (
		('positive', 'Positive'),
		('negative', 'Negative'),
	)
	pd_status = models.CharField(max_length=20, choices=PD_STATUS_CHOICES)
	approximate_preg_months = models.IntegerField()
	vet_recommendation = models.TextField()
	date_of_second_diag = models.DateField(null=True, blank=True)
	FOETUS_STATUS_CHOICES = (
		('progressive', 'Progressive'),
		('non-progressive', 'Non-Progressive'),
	)
	foetus_status = models.CharField(max_length=20, choices=FOETUS_STATUS_CHOICES)
	non_prog_reason=models.CharField(max_length=255,null=True, blank=True,default="")
	action_to_take=models.CharField(max_length=255,null=True, blank=True,default="")
	steaming_up_date=models.DateField(null=True, blank=True)
	expected_dob=models.DateField(null=True, blank=True)
	actual_date_of_delivery=models.DateField(null=True, blank=True)

	def __str__(self):
		return self.name + ' - ' + str(self.id)

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
		balance = models.DecimalField('Balance', max_digits=10, decimal_places=2)
		billing_details=models.CharField('Company', max_length=255)
		comment = models.TextField('Comment', blank=True)
		def __str__(self):
			return self.amount + ' - ' + str(self.id)
		
class Archaricides(models.Model):
		user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
		date_of_purchase = models.DateField('Date of Purchase')
		chemical_name = models.CharField('Chemical Name', max_length=30)
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
		company = models.CharField('Company', max_length=255)
		cost = models.DecimalField('Cost', max_digits=10, decimal_places=2)
		source=models.CharField('Source', max_length=255)
		comment = models.TextField('Comment', blank=True)

		def __str__(self):
			return self.date_of_purchase + ' - ' + str(self.id)

class DairyHygiene(models.Model):
		user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
		chemical_name=models.CharField('Chemical Name', max_length=255)
		date_of_purchase = models.DateField('Date of Purchase')
		item_purchased = models.CharField('Item', max_length=255)
		company = models.CharField('Company', max_length=255)
		quantity=models.CharField('quantity', max_length=255)
		cost = models.DecimalField('Cost', max_digits=10, decimal_places=2)
		expiry_date = models.DateField('Expiry Date')
		comment = models.TextField('Comment', blank=True)

		def __str__(self):
			return self.date_of_purchase + ' - ' + str(self.id)
		
class Salaries(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	category=models.CharField('Category', max_length=255)
	name=models.CharField('Name', max_length=255)
	identification=models.CharField('identification', max_length=255)
	mode_of_payment=models.CharField('Mode', max_length=255)
	amount=models.DecimalField('Amount', max_digits=10, decimal_places=2)
	balance=models.DecimalField('Cost', max_digits=10, decimal_places=2)
	payment_date= models.DateField('Payment Date')
	payment_type=models.CharField('Type', max_length=255)
	comment = models.TextField('Comment', blank=True)


	def __str__(self):
			return self.name + ' - ' + str(self.id)
	
class LivestockInsurance(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	number_insured=models.DecimalField('Number Insured', max_digits=10, decimal_places=2)
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
			('Hormones', 'Hormones'),
			
		]
	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
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
	country = models.CharField(max_length=50)
	district = models.CharField(max_length=50)
	village = models.CharField(max_length=50)
	next_of_kin = models.CharField(max_length=100)
	next_of_kin_phone_no = models.CharField(max_length=15)
	area_of_residence = models.CharField(max_length=100)
	chief_phone_no = models.CharField(max_length=15)
	employee_position = models.CharField(max_length=50)
	salary = models.DecimalField(max_digits=10, decimal_places=2)
	payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS)
	bank_account = models.CharField(max_length=30, blank=True, null=True)
	mode_of_employment = models.CharField(max_length=20, choices=EMPLOYMENT_MODES)
	contract_rewal_period = models.IntegerField(help_text='Contract renewal period in months')

	def __str__(self):
		return self.employee_name+ ' - ' + str(self.id)
	

class LactatingCow(models.Model):
	LACTATION_STAGE_CHOICES = [
		('early', 'Early'),
		('mid', 'Mid'),
		('late', 'Late'),
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
	cow_name = models.CharField(max_length=100)
	reg_no = models.CharField(max_length=50, unique=True)
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
	cow_name = models.ForeignKey(LactatingCow, on_delete=models.CASCADE)
	employee_name = models.ForeignKey(Employees, on_delete=models.CASCADE)
	date = models.DateField()
	time_of_milking = models.CharField(max_length=10, choices=TIME_OF_MILKING_CHOICES)
	quantity = models.FloatField(help_text="Amount of milk in liters")

	def __str__(self):
		return f"{self.date} - {self.cow_name} - {self.time_of_milking}"
class WeeklyMilkRecord(models.Model):
	
	cow_name = models.ForeignKey(LactatingCow, on_delete=models.CASCADE)
	week_start_date = models.DateField()
	total_quantity = models.FloatField(help_text="Total milk in liters for the week")
	#user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return f"Week starting {self.week_start_date} - {self.cow_name}"

class MonthlyMilkRecord(models.Model):
	
	cow_name = models.ForeignKey(LactatingCow, on_delete=models.CASCADE)
	month = models.DateField()
	total_quantity = models.FloatField(help_text="Total milk in liters for the month")
	user = models.ForeignKey(User, on_delete=models.CASCADE)

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


	


	

