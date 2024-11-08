from django.shortcuts import render, redirect
from user.models import *
from .forms import *
import requests
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test,login_required
from .models import *
from django.views import View
from .render import Render
from django.utils import timezone
from django.core.serializers import serialize
from django.http import FileResponse
from fpdf import FPDF
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
import json
from .monitoring import *
from io import BytesIO
from .serializers import *
from rest_framework import generics
from .pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated
from .permissions import Is_Farmer,Is_Vet
from rest_framework.response import Response
from django.db.models import OuterRef, Subquery
from datetime import timedelta,time
from rest_framework.exceptions import ValidationError
from django.core.exceptions import MultipleObjectsReturned
import logging
from django.db import transaction
from rest_framework import generics,status



logger = logging.getLogger(__name__)


def vet_check(request):
    return request.is_vet_officer

def farmer_check(request):
    return request.is_farmer
def official_check(request):
    return request.is_official



@user_passes_test(vet_check, login_url='vet-login')
def portal_vet(request):
    vet_officers = Vet_Officer.objects.all()
    context = {
        'all_vets': vet_officers,
       
    }
    return render(request, 'portals/dashboardVet.html', context)

@user_passes_test(official_check, login_url='official-login')
def portal_official(request):
    officers = Official.objects.all()
    context = {
        'all_officers': officers,
       
    }
    return render(request, 'portals/dashboardOfficial.html', context)
    
    

@user_passes_test(farmer_check, login_url='farmer-login')   
def vet_list(request):
    vet_officers = Vet_Officer.objects.all()
    context = {
        'all_vets': vet_officers,  
    }
    return render(request, 'portals/vetList.html', context)


@user_passes_test(vet_check, login_url='vet-login')
def vet_list_vet(request):
    vet_officers = Vet_Officer.objects.all()
    context = {
        'all_vets': vet_officers,  
    }
    return render(request, 'portals/vet_list_vet.html', context)
    

@user_passes_test(farmer_check, login_url='farmer-login')
def portal_farmer(request):
    vet_officers = Vet_Officer.objects.all()
    context = {
        'all_vets': vet_officers
    }
    return render(request, 'portals/dashboardFarmer.html', context)



def surgical_record(request):
    return render(request, 'portals/reports/surgery.html', {})

def surgical_view(request):
    return render(request, 'portals/reports/surgeryview.html', {})

class SurgicalRecordCreate(generics.CreateAPIView):
    queryset = SurgicalRecord.objects.all()
    serializer_class = SurgicalRecordSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SurgicalRecordList(generics.ListAPIView):
    serializer_class = SurgicalRecordSerializer
    permission_classes = [Is_Vet | Is_Farmer]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
           
            return SurgicalRecord.objects.filter(user=user)
        
        elif user.is_farmer:
            
            return SurgicalRecord.objects.filter(assigned_to=user)

        return SurgicalRecord.objects.none()

    
class SurgicalRecordUpdate(generics.UpdateAPIView):
    queryset = SurgicalRecord.objects.all()
    serializer_class = SurgicalRecordSerializer
    permission_classes = [Is_Vet]

class SurgicalRecordDelete(generics.DestroyAPIView):
    queryset = SurgicalRecord.objects.all()
    serializer_class = SurgicalRecordSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

def vetbilling(request):
    return render(request, 'portals/reports/veterinarybilling.html', {})
def vetbilling_view(request):
    return render(request, 'portals/reports/vetbillsview.html', {})

class VeterinaryBillingCreate(generics.CreateAPIView):
    queryset = VeterinaryBilling.objects.all()
    serializer_class = VeterinaryBillingSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        # Add any custom behavior here if needed
        serializer.save(user=self.request.user)

class VeterinaryBillingList(generics.ListAPIView):
    serializer_class = VeterinaryBillingSerializer
    permission_classes = [Is_Vet|Is_Farmer]
    pagination_class = CustomPagination  # Assuming you have a custom pagination class

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
           
            return VeterinaryBilling.objects.filter(user=user)
        
        elif user.is_farmer:
            
            return VeterinaryBilling.objects.filter(assigned_to=user)

        return VeterinaryBilling.objects.none()
class VeterinaryBillingUpdate(generics.UpdateAPIView):
    queryset = VeterinaryBilling.objects.all()
    serializer_class = VeterinaryBillingSerializer
    permission_classes = [Is_Vet]

class VeterinaryBillingDelete(generics.DestroyAPIView):
    queryset = VeterinaryBilling.objects.all()
    serializer_class = VeterinaryBillingSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

# Deworming Views
def deworming(request):
    return render(request, 'portals/reports/deworming.html', {})
def deworming_view(request):
    return render(request, 'portals/reports/dewormingview.html', {})
class DewormingCreate(generics.CreateAPIView):
    queryset = Deworming.objects.all()
    serializer_class = DewormingSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DewormingList(generics.ListAPIView):
    serializer_class = DewormingSerializer
    permission_classes = [Is_Vet|Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
            user = self.request.user

            if user.is_vet_officer:
            
                return Deworming.objects.filter(user=user)
            
            elif user.is_farmer:
                
                return Deworming.objects.filter(assigned_to=user)

            return Deworming.objects.none()
class DewormingUpdate(generics.UpdateAPIView):
    queryset = Deworming.objects.all()
    serializer_class = DewormingSerializer
    permission_classes = [Is_Vet]

class DewormingDelete(generics.DestroyAPIView):
    queryset = Deworming.objects.all()
    serializer_class = DewormingSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

# ArtificialInsemination Views
def artificial(request):
    return render(request, 'portals/reports/artificialinsemination.html', {})
def artificial_view(request):
    return render(request, 'portals/reports/artificial-inseminationview.html', {})

class ArtificialInseminationCreate(generics.CreateAPIView):
    queryset = ArtificialInsemination.objects.all()
    serializer_class = ArtificialInseminationSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
            #reg_no = self.request.data.get('reg_no')
            #bull_reg_no=self.request.data.get('bull_reg_no')
            user = self.request.user

           
           # if ArtificialInsemination.objects.filter(Q(user=user) & (Q(reg_no=reg_no))).exists():
               # raise ValidationError(f"Record with Registration '{reg_no}' or Bull Registration  already exists!")

            serializer.save(user=user)

class ArtificialInseminationList(generics.ListAPIView):
    serializer_class = ArtificialInseminationSerializer
    permission_classes = [Is_Vet|Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return ArtificialInsemination.objects.filter(user=user).order_by('-farm_name')
        
        elif user.is_farmer:
            return ArtificialInsemination.objects.filter(assigned_to=user).order_by('-farm_name')

        return ArtificialInsemination.objects.none()
    
class ArtificialInseminationUpdate(generics.UpdateAPIView):
    queryset = ArtificialInsemination.objects.all()
    serializer_class = ArtificialInseminationSerializer
    permission_classes = [Is_Vet]

class ArtificialInseminationDelete(generics.DestroyAPIView):
    queryset = ArtificialInsemination.objects.all()
    serializer_class = ArtificialInseminationSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

# PregnancyDiagnosis Views
def pregdiagnosis(request):
    return render(request, 'portals/reports/pregnancydiag.html', {})
def pregdiagnosis_view(request):
    return render(request, 'portals/reports/pregdiagview.html', {})


class PregnancyDiagnosisCreate(generics.CreateAPIView):
    queryset = PregnancyDiagnosis.objects.all()
    serializer_class = PregnancyDiagnosisSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PregnancyDiagnosisList(generics.ListAPIView):
    serializer_class = PregnancyDiagnosisSerializer
    permission_classes = [Is_Vet|Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
           
            return PregnancyDiagnosis.objects.filter(user=user)
        
        elif user.is_farmer:
            
            return PregnancyDiagnosis.objects.filter(assigned_to=user)

        return PregnancyDiagnosis.objects.none()
    
class PregnancyDiagnosisUpdate(generics.UpdateAPIView):
    queryset = PregnancyDiagnosis.objects.all()
    serializer_class = PregnancyDiagnosisSerializer
    permission_classes = [Is_Vet]

class PregnancyDiagnosisDelete(generics.DestroyAPIView):
    queryset = PregnancyDiagnosis.objects.all()
    serializer_class = PregnancyDiagnosisSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

# FarmConsultation Views
def consultation(request):
    return render(request, 'portals/reports/farmconsultation.html', {})

def consultation_view(request):
    return render(request, 'portals/reports/farmconsultationview.html', {})

class FarmConsultationCreate(generics.CreateAPIView):
    queryset = FarmConsultation.objects.all()
    serializer_class = FarmConsultationSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FarmConsultationList(generics.ListAPIView):
    serializer_class = FarmConsultationSerializer
    permission_classes = [Is_Vet|Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
           
            return FarmConsultation.objects.filter(user=user)
        
        elif user.is_farmer:
            
            return FarmConsultation.objects.filter(assigned_to=user)

        return FarmConsultation.objects.none()
    
class FarmConsultationUpdate(generics.UpdateAPIView):
    queryset = FarmConsultation.objects.all()
    serializer_class = FarmConsultationSerializer
    permission_classes = [Is_Vet]

class FarmConsultationDelete(generics.DestroyAPIView):
    queryset = FarmConsultation.objects.all()
    serializer_class = FarmConsultationSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

# Referral Views
@user_passes_test(vet_check, login_url='vet-login')
def referral(request):
    return render(request, 'portals/reports/referral.html', {})
def referral_view(request):
    return render(request, 'portals/reports/referralview.html', {})
class ReferralCreate(generics.CreateAPIView):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReferralList(generics.ListAPIView):
    serializer_class = ReferralSerializer
    permission_classes = [Is_Vet|Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
           
            return Referral.objects.filter(user=user)
        
        elif user.is_farmer:
            
            return Referral.objects.filter(assigned_to=user)

        return Referral.objects.none()
class ReferralUpdate(generics.UpdateAPIView):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
    permission_classes = [Is_Vet]

class ReferralDelete(generics.DestroyAPIView):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()


# Define views
@user_passes_test(farmer_check, login_url='farmer-login')
def calf(request):
    return render(request, 'portals/farmer/calf.html', {})

class CalfCreate(generics.CreateAPIView):
    queryset = Calf.objects.all()
    serializer_class = CalfSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
            registration_number = self.request.data.get('registration_number')
            user = self.request.user

            # Check if the employee exists
            if Calf.objects.filter(user=user, registration_number=registration_number).exists():
                raise ValidationError(f"Calf with Registration '{registration_number}' already exists!")

            serializer.save(user=user)

class CalfList(generics.ListAPIView):
    serializer_class = CalfSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        ###print(user)
        return Calf.objects.filter(user=self.request.user).order_by('-id')
    

class CalfUpdate(generics.UpdateAPIView):
    queryset = Calf.objects.all()
    serializer_class = CalfSerializer
    permission_classes = [Is_Farmer]


class CalfDelete(generics.DestroyAPIView):
    queryset = Calf.objects.all()
    serializer_class = CalfSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

@user_passes_test(farmer_check, login_url='farmer-login')
def dead_animal(request):
    return render(request, 'portals/farmer/dead.html', {})

class DeadAnimalCreate(generics.CreateAPIView):
    queryset = DeadAnimal.objects.all()
    serializer_class = DeadAnimalSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DeadAnimalList(generics.ListAPIView):
    serializer_class = DeadAnimalSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        ###print(user)
        return DeadAnimal.objects.filter(user=self.request.user).order_by('-id')
    

class DeadAnimalUpdate(generics.UpdateAPIView):
    queryset = DeadAnimal.objects.all()
    serializer_class = DeadAnimalSerializer
    permission_classes = [Is_Farmer]


class DeadAnimalDelete(generics.DestroyAPIView):
    queryset = DeadAnimal.objects.all()
    serializer_class = DeadAnimalSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

###Culling
@user_passes_test(farmer_check, login_url='farmer-login')
def culling(request):
    return render(request, 'portals/farmer/culling.html', {})

class CullingCreate(generics.CreateAPIView):
    queryset = Culling.objects.all()
    serializer_class = CullingSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CullingList(generics.ListAPIView):
    serializer_class = CullingSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        ###print(user)
        return Culling.objects.filter(user=self.request.user).order_by('-id')
    

class CullingUpdate(generics.UpdateAPIView):
    queryset = Culling.objects.all()
    serializer_class = CullingSerializer
    permission_classes = [Is_Farmer]


class CullingDelete(generics.DestroyAPIView):
    queryset = Culling.objects.all()
    serializer_class = CullingSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

# livestock inventory
@user_passes_test(farmer_check, login_url='farmer-login')
def livestock(request):
    return render(request, 'portals/farmer/livestock.html', {})
class LivestockCreate(generics.CreateAPIView):
    queryset = Livestock.objects.all()
    serializer_class = LivestockSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LivestockList(generics.ListAPIView):
    serializer_class = LivestockSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        ###print(user)
        return Livestock.objects.filter(user=self.request.user).order_by('-id')
    

class LivestockUpdate(generics.UpdateAPIView):
    queryset = Livestock.objects.all()
    serializer_class = LivestockSerializer
    permission_classes = [Is_Farmer]


class LivestockDelete(generics.DestroyAPIView):
    queryset = Livestock.objects.all()
    serializer_class = LivestockSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

##new animal
@user_passes_test(farmer_check, login_url='farmer-login')
def new_animal(request):
    return render(request, 'portals/farmer/new.html', {})
class NewAnimalCreate(generics.CreateAPIView):
    queryset = NewAnimal.objects.all()
    serializer_class = NewAnimalSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
            reg_no = self.request.data.get('reg_no')
            user = self.request.user

            # Check if the employee exists
            if NewAnimal.objects.filter(user=user, reg_no=reg_no).exists():
                raise ValidationError(f"Animal With with Registration '{reg_no}' already exists!")

            serializer.save(user=user)
class NewAnimalList(generics.ListAPIView):
    serializer_class = NewAnimalSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        ###print(user)
        return NewAnimal.objects.filter(user=self.request.user).order_by('-id')
    

class NewAnimalUpdate(generics.UpdateAPIView):
    queryset = NewAnimal.objects.all()
    serializer_class = NewAnimalSerializer
    permission_classes = [Is_Farmer]


class NewAnimalDelete(generics.DestroyAPIView):
    queryset = NewAnimal.objects.all()
    serializer_class = NewAnimalSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

##############################
@user_passes_test(farmer_check, login_url='farmer-login')
def animal_sales(request):
    return render(request, 'portals/farmer/sales.html', {})

class AnimalSaleCreate(generics.CreateAPIView):
    queryset = AnimalSale.objects.all()
    serializer_class = AnimalSaleSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AnimalSaleList(generics.ListAPIView):
    serializer_class = AnimalSaleSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        ###print(user)
        return AnimalSale.objects.filter(user=self.request.user).order_by('-id')
    

class AnimalSaleUpdate(generics.UpdateAPIView):
    queryset = AnimalSale.objects.all()
    serializer_class = AnimalSaleSerializer
    permission_classes = [Is_Farmer]


class AnimalSaleDelete(generics.DestroyAPIView):
    queryset = AnimalSale.objects.all()
    serializer_class = AnimalSaleSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

@user_passes_test(farmer_check, login_url='farmer-login')
def minerals(request):
    return render(request, 'portals/farmer/minerals.html', {})
class MineralsCreate(generics.CreateAPIView):
    queryset = Minerals.objects.all()
    serializer_class = MineralsSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MineralsList(generics.ListAPIView):
    serializer_class = MineralsSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return Minerals.objects.filter(user=user).order_by('-id')

class MineralsUpdate(generics.UpdateAPIView):
    queryset = Minerals.objects.all()
    serializer_class = MineralsSerializer
    permission_classes = [Is_Farmer]

class MineralsDelete(generics.DestroyAPIView):
    queryset = Minerals.objects.all()
    serializer_class = MineralsSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()  
@user_passes_test(farmer_check, login_url='farmer-login')
def vet_bills(request):
    return render(request, 'portals/farmer/bills.html', {})
class VeterinaryBillsCreate(generics.CreateAPIView):
    queryset = VeterinaryBills.objects.all()
    serializer_class = VeterinaryBillsSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class VeterinaryBillsList(generics.ListAPIView):
    serializer_class = VeterinaryBillsSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination  # If you have a custom pagination class

    def get_queryset(self):
        user = self.request.user
        return VeterinaryBills.objects.filter(user=user).order_by('-id')

class VeterinaryBillsUpdate(generics.UpdateAPIView):
    queryset = VeterinaryBills.objects.all()
    serializer_class = VeterinaryBillsSerializer
    permission_classes = [Is_Farmer]

class VeterinaryBillsDelete(generics.DestroyAPIView):
    queryset = VeterinaryBills.objects.all()
    serializer_class = VeterinaryBillsSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
@user_passes_test(farmer_check, login_url='farmer-login')
def archaricides(request):
    return render(request, 'portals/farmer/archaricides.html', {})

class ArcharicidesCreate(generics.CreateAPIView):
    queryset = Archaricides.objects.all()
    serializer_class = ArcharicidesSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ArcharicidesList(generics.ListAPIView):
    serializer_class = ArcharicidesSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination  # If you have a custom pagination class

    def get_queryset(self):
        user = self.request.user
        return Archaricides.objects.filter(user=user).order_by('-id')

class ArcharicidesUpdate(generics.UpdateAPIView):
    queryset = Archaricides.objects.all()
    serializer_class = ArcharicidesSerializer
    permission_classes = [Is_Farmer]

class ArcharicidesDelete(generics.DestroyAPIView):
    queryset = Archaricides.objects.all()
    serializer_class = ArcharicidesSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
@user_passes_test(farmer_check, login_url='farmer-login')
def equipment(request):
    return render(request, 'portals/farmer/equipment.html', {})
class DairyEquipmentCreate(generics.CreateAPIView):
    queryset = DairyEquipment.objects.all()
    serializer_class = DairyEquipmentSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DairyEquipmentList(generics.ListAPIView):
    serializer_class = DairyEquipmentSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination  # If you have a custom pagination class

    def get_queryset(self):
        user = self.request.user
        return DairyEquipment.objects.filter(user=user).order_by('-id')

class DairyEquipmentUpdate(generics.UpdateAPIView):
    queryset = DairyEquipment.objects.all()
    serializer_class = DairyEquipmentSerializer
    permission_classes = [Is_Farmer]

class DairyEquipmentDelete(generics.DestroyAPIView):
    queryset = DairyEquipment.objects.all()
    serializer_class = DairyEquipmentSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
@user_passes_test(farmer_check, login_url='farmer-login')
def hygiene(request):
    return render(request, 'portals/farmer/hygiene.html', {})
class DairyHygieneCreate(generics.CreateAPIView):
    queryset = DairyHygiene.objects.all()
    serializer_class = DairyHygieneSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DairyHygieneList(generics.ListAPIView):
    serializer_class = DairyHygieneSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination  # If you have a custom pagination class

    def get_queryset(self):
        user = self.request.user
        return DairyHygiene.objects.filter(user=user).order_by('-id')

class DairyHygieneUpdate(generics.UpdateAPIView):
    queryset = DairyHygiene.objects.all()
    serializer_class = DairyHygieneSerializer
    permission_classes = [Is_Farmer]

class DairyHygieneDelete(generics.DestroyAPIView):
    queryset = DairyHygiene.objects.all()
    ##print(queryset)
    serializer_class = DairyHygieneSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

@user_passes_test(farmer_check, login_url='farmer-login')
def salaries(request):
    return render(request, 'portals/farmer/salaries.html', {})
class SalariesCreate(generics.CreateAPIView):
    queryset = Salaries.objects.all()
    #print(queryset)
    serializer_class = SalariesSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
            identification = self.request.data.get('identification')
            user = self.request.user

            # Check if the employee exists
            if Salaries.objects.filter(user=user, identification=identification).exists():
                raise ValidationError(f"Employee with ID '{identification}' already exists!")

            serializer.save(user=user)

class SalariesList(generics.ListAPIView):
    serializer_class = SalariesSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination
    

    def get_queryset(self):
        user = self.request.user
        return Salaries.objects.filter(user=user).order_by('-id')

class SalariesUpdate(generics.UpdateAPIView):
    queryset = Salaries.objects.all()
    serializer_class = SalariesSerializer
    permission_classes = [Is_Farmer]

class SalariesDelete(generics.DestroyAPIView):
    queryset = Salaries.objects.all()
    serializer_class = SalariesSerializer
    permission_classes = [Is_Farmer]           

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
@user_passes_test(farmer_check, login_url='farmer-login')
def insurance(request):
    return render(request, 'portals/farmer/insurance.html', {})
class LivestockInsuranceCreate(generics.CreateAPIView):
    queryset = LivestockInsurance.objects.all()
    serializer_class = LivestockInsuranceSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LivestockInsuranceList(generics.ListAPIView):
    serializer_class = LivestockInsuranceSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination  # If you have a custom pagination class

    def get_queryset(self):
        user = self.request.user
        return LivestockInsurance.objects.filter(user=user).order_by('-id')

class LivestockInsuranceUpdate(generics.UpdateAPIView):
    queryset = LivestockInsurance.objects.all()
    serializer_class = LivestockInsuranceSerializer
    permission_classes = [Is_Farmer]

class LivestockInsuranceDelete(generics.DestroyAPIView):
    queryset = LivestockInsurance.objects.all()
    serializer_class = LivestockInsuranceSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
@user_passes_test(farmer_check, login_url='farmer-login')
def drugs(request):
    return render(request, 'portals/farmer/drugs.html', {})
class VeterinaryDrugsCreate(generics.CreateAPIView):
    queryset = VeterinaryDrugs.objects.all()
    serializer_class = VeterinaryDrugsSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class VeterinaryDrugsList(generics.ListAPIView):
    serializer_class = VeterinaryDrugsSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination  # If you have a custom pagination class

    def get_queryset(self):
        user = self.request.user
        return VeterinaryDrugs.objects.filter(user=user).order_by('-id')

class VeterinaryDrugsUpdate(generics.UpdateAPIView):
    queryset = VeterinaryDrugs.objects.all()
    serializer_class = VeterinaryDrugsSerializer
    permission_classes = [Is_Farmer]

class VeterinaryDrugsDelete(generics.DestroyAPIView):
    queryset = VeterinaryDrugs.objects.all()
    serializer_class = VeterinaryDrugsSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
         
def pdf_notes(request):
    return render(request, 'portals/farmer/pdfnotes.html', {})

@user_passes_test(farmer_check, login_url='farmer-login')
def employees(request):
    return render(request, 'portals/farmer/employment.html', {})

class EmployeesCreate(generics.CreateAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
            id_no = self.request.data.get('id_no')
            user = self.request.user

            # Check if the employee exists
            if Employees.objects.filter(user=user, id_no=id_no).exists():
                raise ValidationError(f"Employee with ID '{id_no}' already exists!")

            serializer.save(user=user)

class EmployeesList(generics.ListAPIView):
    serializer_class = EmployeesSerializer
    permission_classes = [Is_Farmer]  
    pagination_class = CustomPagination  

    def get_queryset(self):
        user = self.request.user
        params = dict()
        if self.request.GET.get('id_no',False):
            
            params['id_no'] = self.request.GET.get('id_no')
            print(params)
        return Employees.objects.filter(user=user,**params).order_by('-id')
class EmployeesUpdate(generics.UpdateAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer
    permission_classes = [Is_Farmer] 

class EmployeesDelete(generics.DestroyAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer
    permission_classes = [Is_Farmer] 

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
@user_passes_test(farmer_check, login_url='farmer-login')
def lactation(request):
    return render(request, 'portals/farmer/lactation.html', {})

class LactatingCowCreate(generics.CreateAPIView):
    queryset = LactatingCow.objects.all()
    serializer_class = LactatingCowSerializer
    permission_classes = [Is_Farmer]

    def perform_create(self, serializer):
            cow_name = self.request.data.get('cow_name')
            #print()
            user = self.request.user

            if LactatingCow.objects.filter(user=user, cow_name=cow_name).exists():
                raise ValidationError(f"Cow with Name '{cow_name}' already exists!")

            serializer.save(user=user)

class LactatingCowList(generics.ListAPIView):
    serializer_class = LactatingCowSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        params = dict()
        if self.request.GET.get('cow_name',False):
            params['cow_name'] = self.request.GET.get('cow_name')
        return LactatingCow.objects.filter(user=user,**params).order_by('-id')

class LactatingCowUpdate(generics.UpdateAPIView):
    queryset = LactatingCow.objects.all()
    serializer_class = LactatingCowSerializer
    permission_classes = [Is_Farmer]

class LactatingCowDelete(generics.DestroyAPIView):
    queryset = LactatingCow.objects.all()
    serializer_class = LactatingCowSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
@user_passes_test(farmer_check, login_url='farmer-login')
def milk_record(request):
    return render(request, 'portals/farmer/milk_records.html', {})

class MilkRecordCreate(generics.CreateAPIView):
    queryset = MilkRecord.objects.all()
    serializer_class = MilkRecordSerializer
    permission_classes = [Is_Farmer]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class MilkRecordList(generics.ListAPIView):
    serializer_class = MilkRecordSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return MilkRecord.objects.filter(user=user).order_by('-id')

class MilkRecordUpdate(generics.UpdateAPIView):
    queryset = MilkRecord.objects.all()
    serializer_class = MilkRecordSerializer
    permission_classes =[Is_Farmer]

class MilkRecordDelete(generics.DestroyAPIView):
    queryset = MilkRecord.objects.all()
    serializer_class = MilkRecordSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

@user_passes_test(farmer_check, login_url='farmer-login')
def daily_record(request):
    return render(request, 'portals/farmer/daily_milk.html', {})

class DailyMilkRecordList(generics.ListAPIView):
    serializer_class = DailyMilkRecordSerializer
    permission_classes = [ Is_Farmer]

    def get_queryset(self):
        user = self.request.user

        # Get the latest id for each cow_name for the authenticated user
        subquery = DailyMilkRecord.objects.filter(
            user=user,
            cow_name=OuterRef('cow_name')
        ).order_by('-id').values('id')[:1]

        latest_records = DailyMilkRecord.objects.filter(
            id__in=Subquery(subquery)
        ).order_by('-date')

        return latest_records
    
class DailyMilkRecordDelete(generics.DestroyAPIView):
    queryset = MilkRecord.objects.all()
    serializer_class = DailyMilkRecordSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
@user_passes_test(farmer_check, login_url='farmer-login')
def weekly_record(request):
    return render(request, 'portals/farmer/weekly_records.html', {})
class WeeklyMilkRecordListView(generics.ListAPIView):
    serializer_class = WeeklyMilkRecordSerializer
    permission_classes = [Is_Farmer]

    def get_queryset(self):
        user = self.request.user

        # Get the MilkRecord instances created by the user
        milk_record_queryset = MilkRecord.objects.filter(user=user)

        # Get the WeeklyMilkRecord instances that are related to the MilkRecord instances created by the user
        return WeeklyMilkRecord.objects.filter(
            cow_name__in=Subquery(milk_record_queryset.values('cow_name'))
        ).order_by('-week_start_date')
class WeeklyMilkRecordDelete(generics.DestroyAPIView):
    queryset = MilkRecord.objects.all()
    serializer_class = WeeklyMilkRecordSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
@user_passes_test(farmer_check, login_url='farmer-login')
def monthly_record(request):
    return render(request, 'portals/farmer/monthly_records.html', {})
class MonthlyMilkRecordListView(generics.ListAPIView):
    serializer_class = MonthlyMilkRecordSerializer
    permission_classes = [Is_Farmer]

    def get_queryset(self):
        user = self.request.user
        return MonthlyMilkRecord.objects.filter(user=user).order_by('-month')
    

class MonthlyMilkRecordDelete(generics.DestroyAPIView):
    queryset = MilkRecord.objects.all()
    serializer_class = MonthlyMilkRecordSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
@user_passes_test(farmer_check, login_url='farmer-login')
def sales_of_milk(request):
    return render(request, 'portals/farmer/milk_sales.html', {})

class SalesOfMilkCreate(generics.CreateAPIView):
    queryset = SalesOfMilk.objects.all()
    serializer_class = SalesOfMilkSerializer
    permission_classes = [Is_Farmer]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SalesOfMilkList(generics.ListAPIView):
    serializer_class = SalesOfMilkSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return SalesOfMilk.objects.filter(user=user).order_by('-id')

class SalesOfMilkUpdate(generics.UpdateAPIView):
    queryset = SalesOfMilk.objects.all()
    serializer_class = SalesOfMilkSerializer
    permission_classes = [Is_Farmer]

class SalesOfMilkDelete(generics.DestroyAPIView):
    queryset = SalesOfMilk.objects.all()
    serializer_class = SalesOfMilkSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

def lab_record(request):
    return render(request, 'portals/reports/laboratory.html', {})

def lab_record_view(request):
    return render(request, 'portals/reports/laboratoryview.html', {})
class LaboratoryRecordCreate(generics.CreateAPIView):
    queryset = LaboratoryRecord.objects.all()
    serializer_class = LaboratoryRecordSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LaboratoryRecordList(generics.ListAPIView):
    serializer_class = LaboratoryRecordSerializer
    permission_classes = [Is_Vet|Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
           
            return LaboratoryRecord.objects.filter(user=user)
        
        elif user.is_farmer:
            
            return LaboratoryRecord.objects.filter(assigned_to=user)

        return LaboratoryRecord.objects.none()
    
class LaboratoryRecordUpdate(generics.UpdateAPIView):
    queryset = LaboratoryRecord.objects.all()
    serializer_class = LaboratoryRecordSerializer
    permission_classes = [Is_Vet]

class LaboratoryRecordDelete(generics.DestroyAPIView):
    queryset = LaboratoryRecord.objects.all()
    serializer_class = LaboratoryRecordSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()


def incidence_record(request):
    return render(request, 'portals/reports/incidence.html', {})
    
def incidence_view(request):
    return render(request, 'portals/reports/incidenceview.html', {})
    
class LivestockIncidentCreate(generics.CreateAPIView):
    queryset = LivestockIncident.objects.all()
    serializer_class = LivestockIncidentSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LivestockIncidentList(generics.ListAPIView):
    serializer_class = LivestockIncidentSerializer
    permission_classes = [Is_Vet|Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
           
            return LivestockIncident.objects.filter(user=user)
        
        elif user.is_farmer:
            
            return LivestockIncident.objects.filter(assigned_to=user)

        return LivestockIncident.objects.none()
class LivestockIncidentUpdate(generics.UpdateAPIView):
    queryset = LivestockIncident.objects.all()
    serializer_class = LivestockIncidentSerializer
    permission_classes = [Is_Vet]

class LivestockIncidentDelete(generics.DestroyAPIView):
    queryset = LivestockIncident.objects.all()
    serializer_class = LivestockIncidentSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

def sample_collection(request):
    return render(request, 'portals/reports/collection.html', {})
def sample_collection_view(request):
    return render(request, 'portals/reports/collectionview.html', {})
class SampleCollectionCreate(generics.CreateAPIView):
    queryset = SampleCollection.objects.all()
    serializer_class = SampleCollectionSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SampleCollectionList(generics.ListAPIView):
    serializer_class = SampleCollectionSerializer
    permission_classes = [Is_Vet|Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
           
            return SampleCollection.objects.filter(user=user)
        
        elif user.is_farmer:
            
            return SampleCollection.objects.filter(assigned_to=user)

        return SampleCollection.objects.none()
    
class SampleCollectionUpdate(generics.UpdateAPIView):
    queryset = SampleCollection.objects.all()
    serializer_class = SampleCollectionSerializer
    permission_classes = [Is_Vet]

class SampleCollectionDelete(generics.DestroyAPIView):
    queryset = SampleCollection.objects.all()
    serializer_class = SampleCollectionSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
            
def sample_processing(request):
    return render(request, 'portals/reports/processing.html', {})
def sample_processing_view(request):
    return render(request, 'portals/reports/processingview.html', {})
class SampleProcessingCreate(generics.CreateAPIView):
    queryset = SampleProcessing.objects.all()
    serializer_class = SampleProcessingSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SampleProcessingList(generics.ListAPIView):
    serializer_class = SampleProcessingSerializer
    permission_classes = [Is_Vet|Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
           
            return SampleProcessing.objects.filter(user=user)
        
        elif user.is_farmer:
            
            return SampleProcessing.objects.filter(assigned_to=user)

        return SampleProcessing.objects.none()
    
class SampleProcessingUpdate(generics.UpdateAPIView):
    queryset = SampleProcessing.objects.all()
    serializer_class = SampleProcessingSerializer
    permission_classes = [Is_Vet]

class SampleProcessingDelete(generics.DestroyAPIView):
    queryset = SampleProcessing.objects.all()
    serializer_class = SampleProcessingSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()


def post_mortem(request):
    return render(request, 'portals/reports/postmortem.html', {})
def post_mortem_view(request):
    return render(request, 'portals/reports/postmortemview.html', {})
class PostMortemRecordCreate(generics.CreateAPIView):
    queryset = PostMortemRecord.objects.all()
    serializer_class = PostMortemRecordSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostMortemRecordList(generics.ListAPIView):
    serializer_class = PostMortemRecordSerializer
    permission_classes = [Is_Vet|Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
           
            return PostMortemRecord.objects.filter(user=user)
        
        elif user.is_farmer:
            
            return PostMortemRecord.objects.filter(assigned_to=user)

        return PostMortemRecord.objects.none()
    
class PostMortemRecordgUpdate(generics.UpdateAPIView):
    queryset = PostMortemRecord.objects.all()
    serializer_class = PostMortemRecordSerializer
    permission_classes = [Is_Vet]

class PostMortemRecordDelete(generics.DestroyAPIView):
    queryset = PostMortemRecord.objects.all()
    serializer_class = PostMortemRecordSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()


def vaccination(request):
    return render(request, 'portals/reports/vaccination.html', {})
def vaccination_view(request):
    return render(request, 'portals/reports/vaccinationview.html', {})
class VaccinationRecordCreate(generics.CreateAPIView):
    queryset = VaccinationRecord.objects.all()
    serializer_class = VaccinationRecordSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class VaccinationRecordList(generics.ListAPIView):
    serializer_class = VaccinationRecordSerializer
    permission_classes = [Is_Vet|Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
           
            return VaccinationRecord.objects.filter(user=user)
        
        elif user.is_farmer:
            
            return VaccinationRecord.objects.filter(assigned_to=user)

        return VaccinationRecord.objects.none()
    
class VaccinationRecordUpdate(generics.UpdateAPIView):
    queryset = VaccinationRecord.objects.all()
    serializer_class = VaccinationRecordSerializer
    permission_classes = [Is_Vet]

class VaccinationRecordDelete(generics.DestroyAPIView):
    queryset = VaccinationRecord.objects.all()
    serializer_class = VaccinationRecordSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
            
            
            
            
def clinical(request):
    return render(request, 'portals/reports/clinical.html', {})
def clinical_view(request):
    return render(request, 'portals/reports/clinicalview.html', {})
class ClinicalRecordCreate(generics.CreateAPIView):
    queryset = ClinicalRecord.objects.all()
    serializer_class = ClinicalRecordSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ClinicalRecordList(generics.ListAPIView):
    serializer_class = ClinicalRecordSerializer
    permission_classes = [Is_Vet | Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        
        if user.is_vet_officer:
            # Vet officers can view records they have created
            return ClinicalRecord.objects.filter(user=user)

        elif user.is_farmer:
            # Farmers can view records assigned to them
            return ClinicalRecord.objects.filter(assigned_to=user)

        return ClinicalRecord.objects.none()


class ClinicalRecordUpdate(generics.UpdateAPIView):
    queryset = ClinicalRecord.objects.all()
    serializer_class = ClinicalRecordSerializer
    permission_classes = [Is_Vet]

    

class ClinicalRecordDelete(generics.DestroyAPIView):
    queryset = ClinicalRecord.objects.all()
    serializer_class = ClinicalRecordSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()


#############Shop############################

def shop(request):
    return render(request, 'portals/shop/myshop.html', {})

def client(request):
    return render(request, 'portals/reports/clients.html', {})

class ClientCreate(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ClientList(generics.ListAPIView):
    serializer_class = ClientSerializer
    permission_classes = [Is_Vet]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        user = self.request.user
        ###print(user)
        return Client.objects.filter(user=self.request.user).order_by('-id')

    


class ClientUpdate(generics.UpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [Is_Vet]


class ClientDelete(generics.DestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
            
            
def diary(request):
    return render(request, 'portals/reports/diary.html', {})

# Class-based view for creating a Diary record
class DiaryCreate(generics.CreateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DiaryList(generics.ListAPIView):
    serializer_class = DiarySerializer
    permission_classes = [Is_Vet ]
    pagination_class = CustomPagination
    def get_queryset(self):
        user = self.request.user
        ###print(user)
        return Diary.objects.filter(user=self.request.user).order_by('-id')

    


class DiaryUpdate(generics.UpdateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [Is_Vet]


class DiaryDelete(generics.DestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

def disease_report(request):
    return render(request, 'portals/reports/disease_report.html', {})

def disease_report_view(request):
    return render(request, 'portals/reports/disease_report_view.html', {})

class DiseaseReportCreate(generics.CreateAPIView):
    queryset = DiseaseReport.objects.all()
    serializer_class = DiseaseReportSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DiseaseReportList(generics.ListAPIView):
    serializer_class = DiseaseReportSerializer
    permission_classes = [Is_Vet | Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return DiseaseReport.objects.filter(user=user)
        
        elif user.is_farmer:
            return DiseaseReport.objects.filter(assigned_to=user)

        return DiseaseReport.objects.none()

class DiseaseReportUpdate(generics.UpdateAPIView):
    queryset = DiseaseReport.objects.all()
    serializer_class = DiseaseReportSerializer
    permission_classes = [Is_Vet]

class DiseaseReportDelete(generics.DestroyAPIView):
    queryset = DiseaseReport.objects.all()
    serializer_class = DiseaseReportSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
            
def resources(request):
    return render(request, 'portals/reports/resources.html', {})

def slaughterhouse(request):
    return render(request, 'portals/reports/slaughter.html', {})

# def slaughterhouse(request):
#     return render(request, 'portals/reports/slaughter_view.html', {})

class SlaughterhouseCreate(generics.CreateAPIView):
    queryset = Slaughterhouse.objects.all()
    serializer_class = SlaughterhouseSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save()

class SlaughterhouseList(generics.ListAPIView):
    serializer_class = SlaughterhouseSerializer
    permission_classes = [Is_Vet | Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return Slaughterhouse.objects.all()
        
        elif user.is_farmer:
            return Slaughterhouse.objects.none()

        return Slaughterhouse.objects.none()

class SlaughterhouseUpdate(generics.UpdateAPIView):
    queryset = Slaughterhouse.objects.all()
    serializer_class = SlaughterhouseSerializer
    permission_classes = [Is_Vet]

class SlaughterhouseDelete(generics.DestroyAPIView):
    queryset = Slaughterhouse.objects.all()
    serializer_class = SlaughterhouseSerializer
    permission_classes = [Is_Vet]


# Employee Views
def employee(request):
    return render(request, 'portals/reports/employee.html', {})
# def employee_view(request):
#     return render(request, 'portals/reports/employee_view.html', {})
class EmployeeCreate(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save()

class EmployeeList(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [Is_Vet]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Employee.objects.all()

class EmployeeUpdate(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [Is_Vet]

class EmployeeDelete(generics.DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [Is_Vet]


# Butcher Views
def butcher(request):
    return render(request, 'portals/reports/butcher.html', {})

# def butcher_view(request):
#     return render(request, 'portals/reports/butcher_view.html', {})
class ButcherCreate(generics.CreateAPIView):
    queryset = Butcher.objects.all()
    serializer_class = ButcherSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save()

class ButcherList(generics.ListAPIView):
    serializer_class = ButcherSerializer
    permission_classes = [Is_Vet | Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return Butcher.objects.all()
        
        elif user.is_farmer:
            return Butcher.objects.none()

        return Butcher.objects.none()

class ButcherUpdate(generics.UpdateAPIView):
    queryset = Butcher.objects.all()
    serializer_class = ButcherSerializer
    permission_classes = [Is_Vet]

class ButcherDelete(generics.DestroyAPIView):
    queryset = Butcher.objects.all()
    serializer_class = ButcherSerializer
    permission_classes = [Is_Vet]


# Invoice Views
def invoice(request):
    return render(request, 'portals/reports/invoice.html', {})

def invoice_view(request):
    return render(request, 'portals/reports/invoiceview.html', {})
class InvoiceCreate(generics.CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save()

class InvoiceList(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [Is_Vet | Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            
            return Invoice.objects.filter()
        
        elif user.is_farmer:
            
            return Invoice.objects.filter(assigned_to=user)

        return Invoice.objects.none()

class InvoiceUpdate(generics.UpdateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [Is_Vet]

class InvoiceDelete(generics.DestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [Is_Vet]
    
    
    
def quiz(request):
    return render(request, 'portals/reports/quiz.html', {})
class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [Is_Vet]
    pagination_class=None

class SubmitAnswerView(generics.CreateAPIView):
    serializer_class = UserAnswerSerializer
    permission_classes = [Is_Vet]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_answer = serializer.save()
            is_correct = user_answer.choice.is_correct
            return Response({'is_correct': is_correct}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def tutorial(request):
    return render(request, 'portals/reports/cpd.html', {})
def lesson(request):
    return render(request, 'portals/reports/lessons.html', {})
    
class TutorialCreate(generics.CreateAPIView):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    permission_classes = [Is_Vet]

class TutorialList(generics.ListAPIView):
    serializer_class = TutorialSerializer
    permission_classes = [Is_Vet]
    
    def get_queryset(self):
        return Tutorial.objects.all().order_by('-created_at')

class TutorialUpdate(generics.UpdateAPIView):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    permission_classes = [Is_Vet]

class TutorialDelete(generics.DestroyAPIView):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        instance.delete()

class SectionCreate(generics.CreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [Is_Vet]

# class SectionList(generics.ListAPIView):
#     serializer_class = SectionSerializer
#     permission_classes = [Is_Vet]

#     def get_queryset(self):
#         lesson_id = self.kwargs['lesson_id']
#         return Section.objects.filter(lesson_id=lesson_id).order_by('-id')

class SectionList(View):
    permission_classes = [Is_Vet]
    pagination_class=None

    def get(self, request, lesson_id):
        sections = Section.objects.filter(lesson_id=lesson_id).order_by('-id')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            serializer = SectionSerializer(sections, many=True)
            return Response(serializer.data)
        context = {
            'sections': sections,
            'lesson_id': lesson_id  
        }
        return render(request, 'portals/reports/lessons.html', context)
    
    
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        section_id = self.kwargs.get('section_id')
        section = Section.objects.get(id=section_id)
        serializer.save(author=self.request.user, section=section)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        section_id = self.kwargs.get('section_id')
        if response.status_code == status.HTTP_201_CREATED:
            return redirect('comment-list', section_id=section_id)
        return response
        
class CommentListView(View):
    permission_classes = [Is_Vet]

    def get(self, request, section_id):
        comments = Comment.objects.filter(section__id=section_id).order_by('-created_at')
        section = Section.objects.get(id=section_id)
        
        context = {
            'comments': comments,
            'section_id': section_id,
        }
        return render(request, 'portals/reports/comments.html',context)
    
    
class QuestionCreateView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        section_id = self.kwargs['section_id']
        section = get_object_or_404(Section, id=section_id)
        serializer.save(section=section)
    
class QuestionDetailView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionsSerializer
    permission_classes = [IsAuthenticated]
    
class SectionQuestionListView(generics.ListAPIView):
    serializer_class = QuestionsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        section_id = self.kwargs['section_id']
        return Question.objects.filter(section_id=section_id)
    
class UserAnswerCreate(generics.CreateAPIView):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')
        section_id = self.request.data.get('section_id')
        answers = self.request.data.get('answers')

        for answer in answers:
            question_id, choice_id = answer.split('-')
            serializer.save(user_id=user_id, question_id=question_id, choice_id=choice_id)