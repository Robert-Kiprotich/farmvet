from django.forms import ModelForm, DateInput,TimeInput,Select,ChoiceField,Textarea,TextInput,NumberInput
from django.contrib.auth import get_user_model
from datetime import timedelta

from portals.models import *

User = get_user_model()
	
class SickApproachForm(ModelForm):
	class Meta:
		model = Sick_Approach_Form
		exclude = ['vet_form', 'vet', 'report_created_on',]

		widgets = {
            'start_dose_date': DateInput(attrs={'type': 'date'}),
        }

	


class DeathApproachForm(ModelForm):
	class Meta:
		model = Death_Approach_Form
		exclude = ['vet_form', 'report_created_on',]

		widgets = {
            'death_date': DateInput(attrs={'type': 'date'}),
			'death_time': TimeInput(attrs={'type':'time'})
        }


class SurgicalApproachForm(ModelForm):
	class Meta:
		model = Surgical_Approach_Form
		exclude = ['vet_form', 'report_created_on',]

		widgets = {
            'operation_date': DateInput(attrs={'type': 'date'}),
        }

class DewormingForm(ModelForm):
	class Meta:
		model = Deworming_Form
		exclude = ['vet_form', 'report_created_on',]

		widgets = {
            'date_of_deworming': DateInput(attrs={'type': 'date'}),
			'next_date_deworming': DateInput(attrs={'type':'date'}),
        }


class VaccinationForm(ModelForm):
	class Meta:
		model = Vaccination_Form
		exclude = ['vet_form', 'report_created_on',]

		
		widgets = {
            'date_of_vaccination': DateInput(attrs={'type': 'date'}),
			'next_date_of_vaccination': DateInput(attrs={'type':'date'}),
        }


class ArtificialInseminationForm(ModelForm):
	class Meta:
		model = Artificial_Insemination_Form
		exclude = ['vet_form', 'report_created_on',]

		widgets = {
			'time_of_heat_sign':TimeInput(attrs={'type':'time'}),
			'time_of_insemination':TimeInput(attrs={'type':'time'}),
            'date_of_insemination': DateInput(attrs={'type': 'date'}),
			'date_of_birth':DateInput(attrs={'type':'date'}),
			'date_of_repeat_checked': DateInput(attrs={'type':'date'}),
			'date_of_pregnancy_diagnosis': DateInput(attrs={'type':'date'}),
			'expected_date_of_calving': DateInput(attrs={'type':'date'}),
        }


class CalfRegistrationForm(ModelForm):
	class Meta:
		model = Calf_Registration_Form
		exclude = ['vet_form', 'report_created_on', 'farmer_username',]

		widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
			'expected_date_of_weaning': DateInput(attrs={'type': 'date'}),
        }


class LivestockInventoryForm(ModelForm):
	class Meta:
		model = Livestock_Inventory_Form
		exclude = ['vet_form', 'report_created_on', 'Attach_photos_of_your_animal']

		widgets = {
            'date_of_culling': DateInput(attrs={'type': 'date'}),
        }


class PregnancyDiagnosisForm(ModelForm):
	class Meta:
		model = Pregnancy_Diagnosis_Form
		exclude = ['vet_form', 'report_created_on',]

		widgets = {
            'date_of_insemination': DateInput(attrs={'type': 'date'}),
			'date_of_pregnancy_diagnosis': DateInput(attrs={'type':'date'}),
			'next_date_of_pregnancy_diagnosis' : DateInput(attrs={'type': 'date'}),
			'expected_date_of_delivery' : DateInput(attrs={'type' : 'date'}),
        }		

class FarmConsultationForm(ModelForm):
	class Meta:
		model = Farm_Consultation
		exclude = ['vet_form', 'report_created_on',]	


class VeterinaryBillingForm(ModelForm):
	class Meta:
		model = Veterinary_Billing_Form
		exclude = ['vet_form', 'report_created_on',]

		widgets = {
            'agreed_date': DateInput(attrs={'type': 'date'}),
        }


class LaboratoryForm(ModelForm):
	class Meta:
		model = Laboratory_Form
		exclude = ['vet_form', 'report_created_on',]

		widgets = {
            'date_of_submission ': DateInput(attrs={'type': 'date'}),
        } 

class ReferalForm(ModelForm):
	class Meta:
		model = Referral_Form
		exclude = ['vet_form', 'report_created_on',]

		widgets = {
            'referal_date': DateInput(attrs={'type': 'date'}),
        } 

class CalfRegForm(ModelForm):
    class Meta:
        model = Calf
        fields = ['name_given', 'birth_date', 'breed', 'gender', 'sire_details', 'color', 'birth_weight', 'medical_conditions', 'registration_number', 'registration_date', 'expected_weaning', 'breeding_level', 'comments']
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'}),
            'registration_date': DateInput(attrs={'type': 'date'}),
            'expected_weaning': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(CalfRegForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class DeadAnimalForm(ModelForm):
    class Meta:
        model = DeadAnimal
        fields = ['name', 'farm_name', 'no_of_affected', 'gender', 'breed', 'sickness_period', 'cause_of_death', 'death_date', 'death_time', 'signs_before_death', 'postmortem_by_vet', 'safety_precaution', 'comment']
        widgets = {
            'gender': Select(choices=[('Male', 'Male'), ('Female', 'Female')]),
            'death_date': DateInput(attrs={'type': 'date'}),
            'death_time': TimeInput(attrs={'type': 'time'}),
            'postmortem_by_vet': Select(choices=[('Yes', 'Yes'), ('No', 'No')]),
            'safety_precaution': Select(choices=[('Burying', 'Burying'), ('Cremation', 'Cremation')]),
        }

    def __init__(self, *args, **kwargs):
        super(DeadAnimalForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class CullingForm(ModelForm):
    class Meta:
        model = Culling
        fields = ['name', 'age', 'gender', 'breed', 'culling_method', 'no_of_culled',
                  'culling_reason', 'reg_no', 'culling_date', 'culling_price', 'comment']
        widgets = {
            'gender': Select(choices=[('Male', 'Male'), ('Female', 'Female')]),
            'culling_date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(CullingForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class LivestockForm(ModelForm):
    class Meta:
        model = Livestock
        fields = '__all__'
        exclude=['user']
        widgets = {
            'date_added': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(LivestockForm, self).__init__(*args, **kwargs)
        self.fields['animal_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['breed_category'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_added'].widget.attrs.update({'class': 'form-control'})
        self.fields['no_of_animals'].widget.attrs.update({'class': 'form-control'})
        self.fields['no_of_males'].widget.attrs.update({'class': 'form-control'})
        self.fields['no_of_females'].widget.attrs.update({'class': 'form-control'})
        self.fields['no_of_adults'].widget.attrs.update({'class': 'form-control'})
        self.fields['no_of_young'].widget.attrs.update({'class': 'form-control'})
        self.fields['no_of_dead'].widget.attrs.update({'class': 'form-control'})
        self.fields['reason_for_death'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})

class NewAnimalForm(ModelForm):
    class Meta:
        model = NewAnimal
        fields = '__all__'
        exclude=['user']
        widgets = {
            'date_added': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(NewAnimalForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['reg_no'].widget.attrs.update({'class': 'form-control'})
        self.fields['source'].widget.attrs.update({'class': 'form-control'})
        self.fields['farmer_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['animal_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['breed'].widget.attrs.update({'class': 'form-control'})
        self.fields['breeding_level'].widget.attrs.update({'class': 'form-control'})
        self.fields['defect'].widget.attrs.update({'class': 'form-control'})
        self.fields['defect_reason'].widget.attrs.update({'class': 'form-control', 'rows': '3'})
        self.fields['animal_color'].widget.attrs.update({'class': 'form-control'})
        self.fields['market_value'].widget.attrs.update({'class': 'form-control'})
        self.fields['medical_history'].widget.attrs.update({'class': 'form-control'})
        self.fields['assessed_by_vet'].widget.attrs.update({'class': 'form-control'})
        self.fields['insured'].widget.attrs.update({'class': 'form-control'})
        self.fields['insuring_company'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_added'].widget.attrs.update({'class': 'form-control'})

class AnimalSaleForm(ModelForm):
    class Meta:
        model = AnimalSale
        fields = '__all__'
        exclude=['user']

    breed = ChoiceField(choices=AnimalSale.BREED_CHOICES, widget=Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(AnimalSaleForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
			
class HeatSignMonitoringForm(ModelForm):
    class Meta:
        model = HeatSignMonitoring
        fields = ['name', 'reg_no', 'status', 'date_of_heat_sign', 'exp_date_of_repeated_heat', 'reason_skip_monitoring']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'reg_no': TextInput(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'date_of_heat_sign':DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'exp_date_of_repeated_heat': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason_skip_monitoring':Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
		
class PregnancyMonitoringForm(ModelForm):
    class Meta:
        model = PregnancyMonitoring
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'reg_no': TextInput(attrs={'class': 'form-control'}),
            'date_of_ai': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'exp_heat_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'first_preg_diag_date':DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pd_status': Select(attrs={'class': 'form-control'}),
            'approximate_preg_months': NumberInput(attrs={'class': 'form-control'}),
            'vet_recommendation': Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_of_second_diag': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'foetus_status':Select(attrs={'class': 'form-control'}),
            'non_prog_reason': TextInput(attrs={'class': 'form-control','required': False}),
            'steaming_up_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
             'expected_dob': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class GestationForm(ModelForm):
    class Meta:
        model = GestationMonitoring
        fields = ['gestation_date']
       

    def save(self, commit=True):
        instance = super(GestationForm, self).save(commit=False)
        gestation_date = instance.gestation_date

        # Calculate repeat date (3 weeks after gestation date)
        instance.repeat_date = gestation_date + timedelta(weeks=3)

        # Calculate expected delivery date (9 months after gestation date)
        instance.expected_delivery_date = gestation_date + timedelta(days=9*30)

        if commit:
            instance.save()
        return instance