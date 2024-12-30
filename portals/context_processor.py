from django.contrib.auth import get_user_model
from .models import *

def all_farmers(request):
    User = get_user_model()
    farmers = User.objects.filter(is_farmer=True).order_by('first_name')
    return {'all_farmers': farmers}
def all_officials(request):
    User = get_user_model()
    officials = User.objects.filter(is_official=True).order_by('first_name')
    return {'all_officials': officials}

def choices(request):
    return {
        'LIVESTOCK_CATEGORY_CHOICES': LaboratoryRecord.LIVESTOCK_CATEGORY_CHOICES,
        'SEX_CHOICES': LaboratoryRecord.SEX_CHOICES,
        'AGE_CHOICES': LaboratoryRecord.AGE_CHOICES,
        'SAMPLE_TYPE_CHOICES': LaboratoryRecord.SAMPLE_TYPE_CHOICES,
        'SAMPLE_RATING_CHOICES': LaboratoryRecord.SAMPLE_RATING_CHOICES,
        'TRANSPORTATION_CHOICES': LaboratoryRecord.TRANSPORTATION_CHOICES,
        'LIVESTOCK_CATEGORY_CHOICES': PostMortemRecord.LIVESTOCK_CATEGORY_CHOICES,
        'SEX_CHOICES': PostMortemRecord.SEX_CHOICES,
        'YES_NO_CHOICES': PostMortemRecord.YES_NO_CHOICES,
        'DISPOSAL_CHOICES': PostMortemRecord.DISPOSAL_CHOICES,
        'CATEGORY_CHOICES': PregnancyDiagnosis.CATEGORY_CHOICES,
        'PD_RESULTS_CHOICES': PregnancyDiagnosis.PD_RESULTS_CHOICES,
        'AREA_OF_INTEREST_CHOICES_FARM': FarmConsultation.AREA_OF_INTEREST_CHOICES,
        'BILLING_CATEGORY_CHOICES': VeterinaryBilling.BILLING_CATEGORY_CHOICES,
        'MODE_OF_PAYMENT_CHOICES': VeterinaryBilling.MODE_OF_PAYMENT_CHOICES,
        'SPECIES_TARGETED_CHOICES':Deworming.SPECIES_TARGETED_CHOICES,
        'SERVED_BY_CHOICES': ArtificialInsemination.SERVED_BY_CHOICES,
        'ABORTION_STATUS_CHOICES': ArtificialInsemination.ABORTION_STATUS_CHOICES,
        'INSEMINATION_STATUS_CHOICES':ArtificialInsemination.INSEMINATION_STATUS_CHOICES,
        'ANIMAL_SPECIES_CHOICES': ClinicalRecord.ANIMAL_SPECIES_CHOICES,
        'DISEASE_NATURE_CHOICES': ClinicalRecord.DISEASE_NATURE_CHOICES,
        'YES_NO_CHOICES': ClinicalRecord.YES_NO_CHOICES,
        'AREA_OF_INTEREST_CHOICES': FarmConsultation.AREA_OF_INTEREST_CHOICES,
        'LIVESTOCK_CATEGORY_CHOICES': SampleProcessing.LIVESTOCK_CATEGORY_CHOICES,
        'SEX_CHOICES': SampleProcessing.SEX_CHOICES,
        'AGE_CHOICES': SampleProcessing.AGE_CHOICES,
        'SAMPLE_RATING_CHOICES': SampleProcessing.SAMPLE_RATING_CHOICES,
        'SAMPLE_COLLECTION_LIVESTOCK_CATEGORY_CHOICES': SampleCollection.LIVESTOCK_CATEGORY_CHOICES,
        'SAMPLE_COLLECTION_SEX_CHOICES': SampleCollection.SEX_CHOICES,
        'SAMPLE_COLLECTION_AGE_CHOICES': SampleCollection.AGE_CHOICES,
        'SAMPLE_COLLECTION_SAMPLE_TYPE_CHOICES': SampleCollection.SAMPLE_TYPE_CHOICES,
        'SAMPLE_COLLECTION_SAMPLE_RATING_CHOICES': SampleCollection.SAMPLE_RATING_CHOICES,
        'SURGICAL_LIVESTOCK_CATEGORIES': SurgicalRecord.LIVESTOCK_CATEGORIES,
        'SURGICAL_SEX_CHOICES': SurgicalRecord.SEX_CHOICES,
        'SURGICAL_AGE_CHOICES': SurgicalRecord.AGE_CHOICES,
        'SURGICAL_NATURE_OF_SURGERY': SurgicalRecord.NATURE_OF_SURGERY,
        'SURGICAL_TYPE_OF_SURGERY': SurgicalRecord.TYPE_OF_SURGERY,
        'SURGICAL_STATUS_CHOICES': SurgicalRecord.STATUS_CHOICES,
        'SURGICAL_PROGNOSIS_CHOICES': SurgicalRecord.PROGNOSIS_CHOICES,
        'VACCINATION_ANIMAL_SPECIES_CHOICES': VaccinationRecord.ANIMAL_SPECIES_CHOICES,
        'VACCINATION_TYPE_CHOICES': VaccinationRecord.VACCINATION_TYPE_CHOICES,
        'NATURE_OF_VACCINATION_PROGRAM_CHOICES': VaccinationRecord.NATURE_OF_VACCINATION_PROGRAM_CHOICES,
        'VACCINATION_SEX':VaccinationRecord.VACCINATION_SEX,
        'BILLING_CATEGORY_CHOICES':VeterinaryBilling.BILLING_CATEGORY_CHOICES,
        'MODE_OF_PAYMENT_CHOICES':VeterinaryBilling.MODE_OF_PAYMENT_CHOICES,
        'LIVESTOCK_CATEGORY_CHOICES':DiseaseReport.LIVESTOCK_CATEGORY_CHOICES,
        'AGE_CHOICES':DiseaseReport.AGE_CHOICES,
        'SEX_CHOICES':DiseaseReport.SEX_CHOICES,
        'YES_NO_CHOICES':DiseaseReport.YES_NO_CHOICES,
        'ASSIGN_TO_CHOICES':Invoice.ASSIGN_TO_CHOICES,
        'INVOICE_CATEGORY_CHOICES':Invoice.INVOICE_CATEGORY_CHOICES,
        'TRANSPORT_CHOICES':Butcher.TRANSPORT_CHOICES,
        'SL_CATEGORY_CHOICES':Slaughterhouse.CATEGORY_CHOICES,
        'E_POSITION_CHOICES':Employee.POSITION_CHOICES,
        'VET_CATEGORY':Practitioner.VET_CATEGORY_CHOICES,
        'SPECIALIZATION':Practitioner.SPECIALIZATION_CHOICES,
        'DISEASE_CHOICES':VaccinationRecord.DISEASE_CHOICES
        
          
    }