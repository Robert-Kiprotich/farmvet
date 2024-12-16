from rest_framework import serializers
from django.db.models import Sum
from datetime import timedelta, date
from .models import *

class PregnancyMonitoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = PregnancyMonitoring
        fields = [
            'id', 'user', 'name', 'reg_no', 'date_of_ai','exp_heat_date','repeat_heat_date',
            'first_preg_diag_date','steaming_up_date', 'expected_dob' 
            
        ]
        read_only_fields = ['exp_heat_date','repeat_heat_date', 'first_preg_diag_date', 'steaming_up_date', 'expected_dob']

class HeatSignMonitoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeatSignMonitoring
        fields = ['id','user','name', 'reg_no', 'status', 'date_of_heat_sign', 'date_of_heat_monitoring','exp_date_of_repeated_heat', 'reason_skip_monitoring']

class AnimalSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalSale
        fields = [
            'id',
            'user',
            'number_sold',
            'name',
            'reg_no',
            'date_sold',
            'age',
            'breed',
            'sex',
            'weight',
            'selling_price',
            'reason',
            'comment',
        ]

class LivestockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livestock
        fields = [
            'id',
            'user',
            'animal_type',
            'breed_category',
            'date_added',
            'no_of_animals',
            'no_of_males',
            'no_of_females',
            'no_of_adults',
            'no_of_young',
            'no_of_dead',
            'reason_for_death',
            'comment'
        ]

class NewAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewAnimal
        fields = [
            'id',
            'user',
            'name',
            'reg_no',
            'source',
            'farmer_name',
            'animal_type',
            'breed',
            'breeding_level',
            'defect',
            'defect_reason',
            'animal_color',
            'market_value',
            'medical_history',
            'assessed_by_vet',
            'insured',
            'insuring_company',
            'date_added'
        ]

class CullingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Culling
        fields = [
            'id',
            'user', 
            'name', 
            'reg_no', 
            'age', 
            'gender',
            'animal_type',
            'breed', 
            'culling_method', 
            'no_of_culled', 
            'culling_reason', 
            'culling_date', 
            'culling_price', 
            'comment'
        ]

class DeadAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeadAnimal
        fields = [
            'id',
            'user', 
            'name', 
            'farm_name', 
            'no_of_affected', 
            'gender', 
            'breed', 
            'sickness_period', 
            'cause_of_death', 
            'death_date', 
            'death_time', 
            'signs_before_death', 
            'postmortem_by_vet', 
            'safety_precaution', 
            'comment'
        ]

class CalfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calf
        fields = [
            'id',
            'user',
            'name_given',
            'registration_number',
            'dam_details',
            'birth_date',
            'breed',
            'gender',
            'sire_details',
            'color',
            'birth_weight',
            'medical_conditions',
            'registration_date',
            'expected_weaning',
            'breeding_level',
            'comments'
        ]

class FeedsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeds
        fields = [
            'id',
            'user',
            'date_of_purchase',
            'feed_type',
            'company',
            'expiry_date',
            'quantity_purchased',
            'trade_name',
            'weight',
            'cost',
            'comment'
        ]


class MineralsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Minerals
        fields = ['id', 'user', 'date_of_purchase', 'mineral_type', 'quantity', 'company', 'expiry_date', 'cost', 'comment']

class VeterinaryBillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VeterinaryBills
        fields = ['id', 'user', 'date_of_billing', 'bill_category', 'amount','amount_billed','balance', 'billing_details', 'comment']
        read_only_fields=['balance']
class ArcharicidesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archaricides
        fields = ['id', 'user', 'date_of_purchase', 'chemical_name','trade_name','quantity', 'company', 'application_rate', 'expiry_date', 'times_used', 'cost', 'comment']

class DairyEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DairyEquipment
        fields = ['id', 'user', 'name','date_of_purchase', 'quantity', 'equipment_type','model_number', 'company', 'cost', 'source', 'comment']

class DairyHygieneSerializer(serializers.ModelSerializer):
    class Meta:
        model = DairyHygiene
        fields = ['id', 'user','chemical_name','trade_name','date_of_purchase', 'item_purchased', 'company', 'quantity', 'cost', 'expiry_date', 'comment']
class SalariesSerializer(serializers.ModelSerializer):
    employee_name = serializers.SlugRelatedField(queryset=Employees.objects.all(), slug_field='id')
    
    class Meta:
        model = Salaries
        fields = ['id', 'user','employee_name', 'employee_position', 'identification', 'mode_of_payment','bank_account','salary_amount','amount', 'balance', 'payment_date', 'payment_type', 'comment']
        read_only_fields = ['bank_account','balance']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        employee_instance = Employees.objects.get(id=data['employee_name'])  
        data['employee_names'] = employee_instance.employee_name 
        print(data)
        return data


class LivestockInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LivestockInsurance
        fields = ['id', 'user', 'number_insured','breed','animal_species','number_insured','company', 'mode_of_payment', 'payment_date', 'total', 'comment']

class VeterinaryDrugsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VeterinaryDrugs
        fields = ['id', 'user','date_of_purchase', 'name', 'category','company','expiry_date', 'strange_condition', 'vet_reg', 'cost', 'comment']

class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = [
            'id',
            'user',
            'employee_name',
            'id_no',
            'phone_no',
            'county',
            'district',
            'village',
            'next_of_kin',
            'next_of_kin_phone_no',
            'chief_name',
            'chief_phone_no',
            'employee_position',
            'salary',
            'payment_method',
            'bank_account',
            'mode_of_employment',
            'contract_rewal_period',
        ]

class LactatingCowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=1)

    class Meta:
        model = LactatingCow
        fields = ['id', 'user', 'cow_name', 'reg_no', 'sire_details', 'breed',
                  'breeding_level', 'age', 'calving_down_date', 'no_of_calves',
                  'average_daily_milk', 'lactation_stage', 'expected_date_of_drying_off']


class MilkRecordSerializer(serializers.ModelSerializer):
    cow_name = serializers.SlugRelatedField(queryset=LactatingCow.objects.all(), slug_field='cow_name')
    employee_name = serializers.SlugRelatedField(queryset=Employees.objects.all(), slug_field='id')
    class Meta:
        model = MilkRecord
        fields = ['id','user', 'cow_name', 'employee_name', 'date', 'time_of_milking', 'quantity']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Concatenate id and employee_name
        employee_instance = Employees.objects.get(id=data['employee_name'])  # Retrieve employee instance using employee_name field
        data['employee_names'] = employee_instance.employee_name 
        #print(data)
        return data
class WeeklyMilkRecordSerializer(serializers.ModelSerializer):
    cow_name = serializers.SlugRelatedField(queryset=LactatingCow.objects.all(), slug_field='cow_name')
    
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = WeeklyMilkRecord
        fields = ['id','cow_name',  'week_start_date', 'total_quantity']

    def get_total_quantity(self, obj):
        week_end_date = obj.week_start_date + timedelta(days=6)
        total_quantity = MilkRecord.objects.filter(
            cow_name=obj.cow_name,
            date__range=[obj.week_start_date, week_end_date]
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0.0
        return total_quantity

class DailyMilkRecordSerializer(serializers.ModelSerializer):
    cow_name = serializers.SlugRelatedField(queryset=LactatingCow.objects.all(), slug_field='cow_name')
    
    class Meta:
        model = DailyMilkRecord
        fields = ['id','cow_name', 'date', 'total_quantity']

class MonthlyMilkRecordSerializer(serializers.ModelSerializer):
    cow_name = serializers.SlugRelatedField(queryset=LactatingCow.objects.all(), slug_field='cow_name')
    
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = MonthlyMilkRecord
        fields = ['id','cow_name', 'month', 'total_quantity']

    def get_total_quantity(self, obj):
        start_date = obj.month.replace(day=1)
        next_month = start_date.month % 12 + 1
        year = start_date.year if next_month > 1 else start_date.year + 1
        end_date = date(year, next_month, 1) - timedelta(days=1)
        total_quantity = MilkRecord.objects.filter(
            cow_name=obj.cow_name,
            date__range=[start_date, end_date]
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0.0
        return total_quantity
    
class SalesOfMilkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOfMilk
        fields = [
            'id',
              'user',  
            'date_of_sales',
            'number_of_cows_milked',
            'total_kgs_milked',
            'milk_sales_to',
            'buyer_contact',
            'price_per_kg',
            'total_cash_received',
            'balance',
            'comment'
        ]

class VeterinaryBillingSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = VeterinaryBilling
        fields = ['id','user','assigned_to', 'billing_category', 'total_amount_billed', 'total_paid', 'balance', 'mode_of_payment',
                  'agreed_date', 'payment_plan', 'farmer_name', 'village', 'contact', 'vet_to_be_paid',
                  'reg_no', 'vet_contact', 'signature', 'stamp', 'comment']
        read_only_fields=['balance']

class DewormingSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = Deworming
        fields = ['id','user','assigned_to', 'species_targeted', 'other', 'no_of_adults', 'no_of_young_ones', 'body_conditions',
                    'deworming_date', 'drug_of_choice', 'parasites', 'withdrawal_period', 'side_effects',
                    'nxt_deworming_date', 'farmer_name', 'village', 'contact', 'vet_name', 'reg_no', 'vet_contact',
                    'signature', 'stamp']

class ArtificialInseminationSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = ArtificialInsemination
        fields = ['id','user','assigned_to','farm_name', 'cow_name', 'reg_no', 'dam_details', 'sire_details', 
                   'no_of_repeats', 'abortion_status', 'time_of_heat_sign', 'date_of_heat_sign','insemination_date',
                  'insemination_time','insemination_status','semen_type','breed_used', 'bull_name', 'bull_reg_no', 'semen_source', 'heat_sign_mtr_date',
                  'repeat_heat_date', 'first_pd_date', 'expected_delivery_date', 'owners_name', 'village', 'contact',
                  'vet_name', 'vet_reg_no', 'vet_contact', 'signature', 'stamp']
        read_only_fields=['heat_sign_mtr_date','repeat_heat_date','first_pd_date','expected_delivery_date']
        
class PregnancyDiagnosisSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = PregnancyDiagnosis
        fields = ['id','user','assigned_to', 'cow_name', 'reg_no', 'category', 'date_of_ai', 'pg_diag_date', 'pd_results',
                  'pd_method', 'positive_pd_months', 'negative_pd_comment', 'pd_nxt_date', 'expctd_delivery_date',
                  'comment', 'owners_name', 'village', 'contact', 'vet_name', 'vet_reg_no', 'vet_contact',
                  'signature', 'stamp']

class FarmConsultationSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = FarmConsultation
        fields = ['id','user','assigned_to', 'area_of_interest', 'other_area_of_interest',  'recommendation', 
                  'give_recommendation', 'manager', 'consultant', 'farmer_name', 'contact', 'village',
                  'vet_name', 'vet_reg_no', 'vet_contact', 'signature', 'stamp', 'comment']

class ReferralSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = Referral
        fields = ['id','user','assigned_to', 'species', 'treatment_duration', 'previous_treatment_state', 'prognosis',
                  'referral_date', 'referral_choice', 'r_vet_name', 'r_vet_contact', 'r_vet_reg_no',
                  'farmer_name', 'village', 'contact', 'vet_name', 'vet_reg_no', 'vet_contact', 'signature',
                  'stamp', 'comment']
        
class SurgicalRecordSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = SurgicalRecord
        fields = [
            'id',
            'user',
            'assigned_to',
            'livestock_category_affected',
            'other_livestock_category',
            'name_of_animal',
            'registration_number',
            'sex_of_animal',
            'age_of_animal',
            'nature_of_surgery',
            'type_of_surgery',
            'other_surgery',
            'status_before_operation',
            'pre_operative_management',
            'date_of_operation',
            'post_operation_management',
            'prognosis_of_patient',
            'comment',
            'owner_name',
            'owner_village',
            'owner_mobile_number',
            'vet_in_charge',
            'vet_registration_number',
            'vet_mobile_number',
            'signature',
            'stamp'
        ]

class SampleCollectionSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = SampleCollection
        fields = [
            'id',
            'user',
            'assigned_to',
            'livestock_category',
            'other_livestock',
            'name_of_animal',
            'registration_number',
            'age_of_animal',
            'sex_of_animal',
            'history_of_animal',
            'clinical_signs_of_animal',
            'type_of_sample_collected',
            'date_of_sampling',
            'sample_storage_condition',
            'means_of_transportation',
            'sample_rating',
            'owner_name',
            'owner_village',
            'owner_mobile_number',
            'vet_in_charge_name',
            'vet_in_charge_registration_number',
            'vet_in_charge_mobile_number',
            'signature',
            'stamp'
        ]

class SampleProcessingSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = SampleProcessing
        fields = [
           'id',  
            'user',
            'assigned_to',
            'livestock_category',
            'sample_type_received',
            'sample_rating',
            'animal_name',
            'registration_number',
            'sex_of_animal',
            'age_of_animal',
            'date_of_reception',
            'date_of_sample_processing',
            'number_of_days_for_processing',
            'date_of_sample_results',
            'laboratory_findings',
            'comment',
            'owner_name',
            'owner_village',
            'owner_mobile_number',
            'lab_technologist_name',
            'lab_technologist_registration_number',
            'lab_technologist_mobile_number',
            'laboratory_name',
            'signature',
            'stamp'
        ]
class LaboratoryRecordSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = LaboratoryRecord
        fields = [
            'id',
            'user',
            'assigned_to',
            'livestock_category',
            'other_livestock',
            'name_of_animal',
            'registration_number',
            'age_of_animal',
            'sex_of_animal',
            'history_of_animal',
            'clinical_signs',
            'type_of_sample_collected',
            'date_of_sampling',
            'sample_storage_condition',
            'means_of_transportation',
            'sample_rating',
            'owner_name',
            'owner_village',
            'owner_mobile_number',
            'vet_in_charge_name',
            'vet_registration_number',
            'vet_mobile_number',
           'signature',
            'stamp'
        ]
class LivestockIncidentSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = LivestockIncident
        fields = [
            'id',
            'user',
            'assigned_to',
            'livestock_category',
            'animal_name',
            'sex',
            'age',
            'case_history',
            'number_of_sick_animals',
            'morbidity_rate',
            'incidence_date',
            'incidence_time',
            'cadaver_signs',
            'open_for_pm',
            'no_pm_reason',
            'path_condition',
            'sample_sent',
            'cause_notifiable',
            'cause_zoonotic',
            'precaution',
            'disposal_way',
        ]
class VaccinationRecordSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = VaccinationRecord
        fields = [
            'id',
            'user',
            'assigned_to',
            'species_targeted',
            'other_species',
            'number_of_animals_vaccinated',
            'age_of_animal',
            'sex_of_animal',
            'breed_of_animal',
            'color_of_animal',
            'other_description',
            'vaccination_of',
            'vaccines_used',
            'batch_number',
            'date_of_vaccination',
            'vaccination_type',
            'next_date_of_vaccination',
            'name_of_rash',
            'village_vaccination_done',
            'nature_of_vaccination_program',
            'name_of_owner',
            'village',
            'contact',
            'name_of_vet_incharge',
            'registration_number',
            'mobile_number',
            'signature',
            'stamp'
        ]

class PostMortemRecordSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = PostMortemRecord
        fields = [
            'id',
            'user',
            'assigned_to',
            'livestock_category',
            'other_livestock',
            'name_of_animal',
            'sex',
            'age',
            'case_history',
            'number_of_sick_animals',
            'number_of_dead',
            'morbidity_rate',
            'date_of_incidence',
            'time_of_incidence',
            'signs_of_cadaver',
            'cadaver_open_for_pm',
            'reasons_for_not_opening',
            'major_pathological_conditions',
            'sample_sent_to_lab',
            'cause_of_death_notifiable',
            'cause_of_death_zoonotic',
            'precautions_if_zoonotic',
            'cadaver_disposed_by',
            'owner_name',
            'owner_village',
            'owner_mobile_number',
            'vet_in_charge_name',
            'vet_in_charge_registration_number',
            'vet_in_charge_mobile_number',
            'signature',
            'stamp'
        ]
        
class ClinicalRecordSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = ClinicalRecord
        fields = [
            'id',
            'user',
            'assigned_to',
            'animal_species_affected',
            'other_species',
            'number_of_animals_sick',
            'name_of_animal_affected',
            'registration_number',
            'age_of_animal',
            'breed_of_animal',
            'nature_of_disease',
            'clinical_signs',
            'differential_diagnosis',
            'final_diagnosis',
            'case_history',
            'treatment_plan',
            'drugs_of_choice',
            'prognosis',
            'date_of_start_dose',
            'final_treatment_date',
            'is_zoonotic',
            'precautions',
            'refer_case_to_other_vet',
            'is_disease_reportable',
            'reason_if_not_reportable',
            'is_disease_notifiable',
            'notified_authority',
            'comment',
            'owner_name',
            'owner_village',
            'owner_contact',
            'vet_in_charge_name',
            'vet_registration_number',
            'vet_contact',
            'vet_signature',
            'rubber_stamp'
        ]
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id','user', 'date_of_enrollment', 'full_name', 'mobile_number', 'location', 'livestock_interest', 'remarks']
        
class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['id','user', 'date','time_of_event', 'main_activity', 'client_contact', 'remarks']
        
class DiseaseReportSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = DiseaseReport
        fields = [
            'id',
            'user',
            'assigned_to',
            'livestock_category',
            'other_livestock_category',
            'number_of_animals_affected',
            'sex_of_animals_affected',
            'age_of_animals_affected',
            'clinical_signs',
            'number_of_dead_animals',
            'propose_control_measures',
            'sample_taken_to_lab',
            'tentative_diagnosis',
            'village_disease_occurred',
            'sub_county',
            'county',
            'owner_name',
            'owner_mobile_number',
            'vet_in_charge_name',
            'vet_registration_number',
            'vet_mobile_number',
            'signature',
            'stamp',
        ]
        

# Slaughterhouse Serializer
class SlaughterhouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slaughterhouse
        fields = [
            'id',
            'user', 
            'name', 
            'county', 
            'sub_county', 
            'location', 
            'slaughterhouse_category', 
            'livestock_slaughtered', 
            'number_of_employees', 
            'roller_mark_number',
            'inspector_name',
            'inspector_registration_number',
            'inspector_employment_number',
            'inspector_mobile_number'
        ]


# Employee Serializer
class EmployeeSerializer(serializers.ModelSerializer):
    slaughterhouse = serializers.StringRelatedField()  

    class Meta:
        model = Employee
        fields = [
            'id', 
            'name', 
            'id_number', 
            'mobile_number', 
            'position', 
            'medical_license_status', 
            'slaughterhouse'  
        ]


# Butcher Serializer
class ButcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Butcher
        fields = [
            'id', 
            'name', 
            'id_number', 
            'mobile_number', 
            'medical_license_status', 
            'livestock_slaughtered', 
            'meat_container_number', 
            'meat_carrier_number', 
            'means_of_transport'
        ]

class InvoiceSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Invoice
        fields = [
            'id',
            'user',
            'assigned_to',
            'invoice_category',
            'date_of_invoice',
            'total_amount_due',
            'farmer_name',
            'village',
            'contact',
            'vet_in_charge_of_invoice',
            'vet_registration_number',
            'vet_contact',
            'signature',
            'stamp'
        ]
        
        
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']

# class UserAnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserAnswer
#         fields = ['id','user', 'question', 'choice']
        
        
#tutorial
        
class ChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']


class SectionSerializer(serializers.ModelSerializer):
    lesson_id = serializers.IntegerField(source='lesson.id', read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'lesson_id', 'lesson', 'title', 'content','file','is_active','created_at']

class TutorialSerializer(serializers.ModelSerializer):
    lesson_data = SectionSerializer(many=True, read_only=True, source='sections')  # Include sections and their lesson_id
    class Meta:
        model = Tutorial
        fields = ['id', 'user', 'lesson', 'lesson_data','cpd_number', 'unit_price', 'points', 'is_active']
        
class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'section', 'author', 'author_name', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        
# class UserAnswersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserAnswers
#         fields = ['user', 'question', 'choice']
#cpd quiz
class CpdChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text','is_correct']

class CpdQuestionsSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'choices']

class QuizResultSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  
    section = serializers.StringRelatedField()  

    class Meta:
        model = QuizResult
        fields = ['id', 'user', 'section', 'score', 'passed', 'timestamp']
        # read_only_fields = ['id', 'timestamp']
       
class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = '__all__'
        
class LivestockExaminationRecordSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = LivestockExaminationRecord
        fields = [
            'id',
            'user',
            'assigned_to',
            'livestock_category',
            'other_category',
            'age_of_animal',
            'breed',
            'sex_of_animal',
            'number_of_animals',
            'origin_of_animal',
            'destination',
            'reason_for_examination',
            'recommendation',
            'owner_name',
            'owner_mobile_number',
            'veterinary_officer_in_charge',
            'registration_number',
            'veterinary_officer_mobile_number',
            'veterinary_officer_signature',
            'created_at',
        ]

class CalvingRecordSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = CalvingRecord
        fields = [
            'id',
            'user',
            'assigned_to',
            'date_of_calving',
            'insemination_date',
            'days_to_calving_down',
            'cow_name',
            'registration_number',
            'calving_procedure',
            'rab_status',
            'hours_for_natural_expulsion',
            'calf_sex',
            'calf_status',
            'reason_for_dead_foetus',
            'comment',
            'created_at',
        ]
class AssessmentRecordSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = AssessmentRecord
        fields = [
            'id',
            'user',
            'assigned_to',
            'livestock_category',
            'other_category',
            'date_of_assessment',
            'name_of_animal',
            'registration_number',
            'color_of_animal',
            'age_of_animal',
            'sex_of_animal',
            'number_of_animals',
            'origin_of_animal',
            'place_of_assessment',
            'destination',
            'reason_for_assessment',
            'recommendation',
            'owner_of_animal',
            'owner_mobile_number',
            'veterinary_practitioner_in_charge',
            'practitioner_registration_number',
            'practitioner_contact',
            'signature_and_stamp',
        ]
        
class DailyKillSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = DailyKill
        fields = [
            'id',
            'user',
            'assigned_to',
            'date',
            'livestock_category',
            'number_of_females_killed',
            'number_of_males_killed',
            'total_kills_per_day',
            'condemnation_done',
            'condemnation_status',
            'comment_by_inspector',
            'inspector_name',
            'inspector_reg_number',
            'inspector_status',
        ]
class MovementPermitSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

 # Displays assigned_to as a string
    class Meta:
        model = MovementPermit
        fields = [
            'id', 'user', 'assigned_to', 'date_of_permit', 'sub_county_district',
            'ward_level', 'authorized_by', 'registration_number', 'phone_number',
            'uploaded_permit'
        ]


class NoObjectionSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())


    class Meta:
        model = NoObjection
        fields = [
            'id', 'user', 'assigned_to', 'date_of_confirmation', 'sub_county_district',
            'ward_level', 'confirmed_by', 'registration_number', 'phone_number',
            'uploaded_no_objection_form'
        ]


class MonthlyReportSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())


    class Meta:
        model = MonthlyReport
        fields = [
            'id', 'user', 'assigned_to', 'date_of_submission', 'sub_county',
            'ward_level', 'submitted_by', 'registration_number', 'phone_number',
            'uploaded_report'
        ]
        
class PractitionerSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())


    class Meta:
        model = Practitioner
        fields = [
            'id',
            'user',
            'assigned_to',
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'county',
            'subcounty',
            'ward',
            'area_of_operation',
            'specialization',
            'vet_category',
            'registration_number',
        ]