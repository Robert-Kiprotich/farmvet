from rest_framework import serializers
from django.db.models import Sum
from datetime import timedelta, date
from .models import *

class PregnancyMonitoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = PregnancyMonitoring
        fields = [
            'id', 'user', 'name', 'reg_no', 'date_of_ai', 'exp_heat_date',
            'first_preg_diag_date', 'pd_status', 'approximate_preg_months',
            'vet_recommendation', 'date_of_second_diag', 'foetus_status',
            'non_prog_reason','action_to_take', 'steaming_up_date', 'expected_dob','actual_date_of_delivery'
        ]

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
            'age', 
            'gender',
            'animal_type',
            'breed', 
            'culling_method', 
            'no_of_culled', 
            'culling_reason', 
            'reg_no', 
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
            'birth_date',
            'breed',
            'gender',
            'sire_details',
            'color',
            'birth_weight',
            'medical_conditions',
            'registration_number',
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
        fields = ['id', 'user', 'date_of_billing', 'bill_category', 'amount', 'balance', 'billing_details', 'comment']
    
class ArcharicidesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archaricides
        fields = ['id', 'user', 'date_of_purchase', 'chemical_name', 'quantity', 'company', 'application_rate', 'expiry_date', 'times_used', 'cost', 'comment']

class DairyEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DairyEquipment
        fields = ['id', 'user', 'name','date_of_purchase', 'quantity', 'equipment_type', 'company', 'cost', 'source', 'comment']

class DairyHygieneSerializer(serializers.ModelSerializer):
    class Meta:
        model = DairyHygiene
        fields = ['id', 'user','chemical_name','date_of_purchase', 'item_purchased', 'company', 'quantity', 'cost', 'expiry_date', 'comment']
class SalariesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salaries
        fields = ['id', 'user', 'category', 'name', 'identification', 'mode_of_payment', 'amount', 'balance', 'payment_date', 'payment_type', 'comment']

class LivestockInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LivestockInsurance
        fields = ['id', 'user', 'number_insured', 'company', 'mode_of_payment', 'payment_date', 'total', 'comment']

class VeterinaryDrugsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VeterinaryDrugs
        fields = ['id', 'user', 'name', 'category','company','expiry_date', 'strange_condition', 'vet_reg', 'cost', 'comment']

class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = [
            'id',
            'user',
            'employee_name',
            'id_no',
            'phone_no',
            'country',
            'district',
            'village',
            'next_of_kin',
            'next_of_kin_phone_no',
            'area_of_residence',
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
    employee_name = serializers.SlugRelatedField(queryset=Employees.objects.all(), slug_field='employee_name')
    

    class Meta:
        model = MilkRecord
        fields = ['id','user', 'cow_name', 'employee_name', 'date', 'time_of_milking', 'quantity']

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