from django.shortcuts import render, redirect
from user.models import *
from .forms import *
import requests
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test,login_required
from rest_framework.decorators import api_view, permission_classes
from .models import *
from django.views import View
from .render import Render
from django.utils import timezone
from django.core.serializers import serialize
from django.http import FileResponse
from fpdf import FPDF
from django.db.models import Q, F
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views import View
import json
import os 
import base64
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .monitoring import *
from io import BytesIO
from .serializers import *
from rest_framework import generics,parsers
from .pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated
from .permissions import Is_Farmer,Is_Vet,Is_Official,IsVetOrOfficial
from rest_framework.response import Response
from django.db.models import OuterRef, Subquery
from datetime import timedelta,time,datetime
from rest_framework.exceptions import ValidationError
from django.core.exceptions import MultipleObjectsReturned
import logging
from django.db import transaction
from rest_framework import generics,status
from django.http import FileResponse, Http404
from django.http import FileResponse, HttpResponseNotFound
import cv2
import numpy as np
from django.conf import settings
from django.templatetags.static import static
from django.utils.timezone import now
from  .credentials import *
from .token import *


logger = logging.getLogger(__name__)


def vet_check(user):
    if not user.is_authenticated:
        return False  
    return getattr(user, 'is_vet_officer', False)

def farmer_check(user):
    if not user.is_authenticated:
        return False  
    return getattr(user, 'is_farmer', False)
def official_check(user):
    if not user.is_authenticated:
        return False
    return user.is_official



@user_passes_test(vet_check, login_url='vet-login')
def portal_vet(request):
    vet_officers = Vet_Officer.objects.all()
    context = {
        'all_vets': vet_officers,
         'role': 'vet',
       
    }
    return render(request, 'portals/dashboardVet.html', context)

@user_passes_test(official_check, login_url='official-login')
def portal_official(request):
    officers = Official.objects.all()
    context = {
        'all_officers': officers,
        'role': 'officer'
       
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
        'all_vets': vet_officers,
        'role': 'farmer'
    }
    print(context)
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
           
            return VeterinaryBilling.objects.filter(user=user).order_by('-id')
        
        elif user.is_farmer:
            
            return VeterinaryBilling.objects.filter(assigned_to=user).order_by('-id')

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
            
                return Deworming.objects.filter(user=user).order_by('-id')
            
            elif user.is_farmer:
                
                return Deworming.objects.filter(assigned_to=user).order_by('-id')

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
def artificial_official_view(request):
    return render(request, 'portals/reports/artificial_official.html', {})
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import F
from .models import ArtificialInsemination
from .permissions import IsVetOrOfficial  # Your custom permission

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsVetOrOfficial])
def ai_record_filter(request):
    try:
        user = request.user

        # 🧑‍⚕️ If vet officer: show records they assigned
        if getattr(user, 'is_vet_officer', False):
            records = ArtificialInsemination.objects.filter(
                assigned_by=user
            ).annotate(
                assigned_to_username=F("assigned_to_official__username")
            ).values(
                "id", "insemination_date", "species", "assigned_to_username"
            )
            return Response({
                "user_type": "vet_officer",
                "records": list(records),
            })

        # 🏛️ If official: show records assigned to them
        elif getattr(user, 'is_official', False):
            records = ArtificialInsemination.objects.filter(
                assigned_to_official=user
            ).annotate(
                assigned_by_username=F("assigned_by__username")
            ).values(
                "id", "insemination_date", "species", "assigned_by_username"
            )
            return Response({
                "user_type": "official",
                "records": list(records),
            })

        return Response({"error": "You do not have access to these records."}, status=403)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

class ArtificialInseminationCreate(generics.CreateAPIView):
    queryset = ArtificialInsemination.objects.all()
    serializer_class = ArtificialInseminationSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
            user = self.request.user
            logger.info(f"Received Data: {self.request.data}")  # Log request data
            serializer.save(user=user)


class ArtificialInseminationList(generics.ListAPIView):
    serializer_class = ArtificialInseminationSerializer
    permission_classes = [Is_Vet | Is_Official | Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return ArtificialInsemination.objects.filter(user=user).order_by('-id')
        if user.is_official:
                return ArtificialInsemination.objects.filter(assigned_to_official=user).order_by('-id')

        if user.is_farmer:
            return ArtificialInsemination.objects.filter(assigned_to=user).order_by('-id')

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
           
            return PregnancyDiagnosis.objects.filter(user=user).order_by('-id')
        
        elif user.is_farmer:
            
            return PregnancyDiagnosis.objects.filter(assigned_to=user).order_by('-id')

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
           
            return FarmConsultation.objects.filter(user=user).order_by('-id')
        
        elif user.is_farmer:
            
            return FarmConsultation.objects.filter(assigned_to=user).order_by('-id')

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
def daily_checks(request):
    return render(request, 'portals/farmer/daily_checks.html', {})

class DailyCheckCreate(generics.CreateAPIView):
    queryset = DailyCheck.objects.all()
    serializer_class = DailyCheckSerializer
    permission_classes = [Is_Farmer]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DailyCheckList(generics.ListAPIView):
    serializer_class = DailyCheckSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        return DailyCheck.objects.filter(user=self.request.user).order_by('-id')

class DailyCheckUpdate(generics.UpdateAPIView):
    queryset = DailyCheck.objects.all()
    serializer_class = DailyCheckSerializer
    permission_classes = [Is_Farmer]

    def get_queryset(self):
        return DailyCheck.objects.filter(user=self.request.user)

class DailyCheckDelete(generics.DestroyAPIView):
    queryset = DailyCheck.objects.all()
    serializer_class = DailyCheckSerializer
    permission_classes = [Is_Farmer]

    def get_queryset(self):
        return DailyCheck.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

def other_expenses_view(request):
    return render(request, 'portals/farmer/other_expenses.html', {})
         
class OtherExpenseCreate(generics.CreateAPIView):
    queryset = OtherExpense.objects.all()
    serializer_class = OtherExpenseSerializer
    permission_classes = [Is_Farmer]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OtherExpenseList(generics.ListAPIView):
    serializer_class = OtherExpenseSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination  # Optional

    def get_queryset(self):
        return OtherExpense.objects.filter(user=self.request.user).order_by('-id')


class OtherExpenseUpdate(generics.UpdateAPIView):
    queryset = OtherExpense.objects.all()
    serializer_class = OtherExpenseSerializer
    permission_classes = [Is_Farmer]


class OtherExpenseDelete(generics.DestroyAPIView):
    queryset = OtherExpense.objects.all()
    serializer_class = OtherExpenseSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
            
@user_passes_test(farmer_check, login_url='farmer-login')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expenses(request):
    user = request.user

    vet_bills = VeterinaryBills.objects.filter(user=user).values('id', 'date_of_billing', 'amount')
    archaricides = Archaricides.objects.filter(user=user).values('id', 'date_of_purchase', 'cost')
    hygiene = DairyHygiene.objects.filter(user=user).values('id', 'date_of_purchase', 'cost')
    salaries = Salaries.objects.filter(user=user).values('id', 'payment_date', 'amount')
    feeds = Feeds.objects.filter(user=user).values('id', 'date_of_purchase', 'cost')
    equipment = DairyEquipment.objects.filter(user=user).values('id', 'date_of_purchase', 'cost')
    drugs = VeterinaryDrugs.objects.filter(user=user).values('id', 'date_of_purchase', 'cost')
    minerals = Minerals.objects.filter(user=user).values('id', 'date_of_purchase', 'cost')
    insurance = LivestockInsurance.objects.filter(user=user).values('id', 'payment_date', 'total')
    calving=CalvingRecord.objects.filter(user=user).values('id','date_of_calving','calf_sex')
    other=OtherExpense.objects.filter(user=user).values('id','date','cost')

    vet_bills_total = VeterinaryBills.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    archaricides_total = Archaricides.objects.filter(user=user).aggregate(Sum('cost'))['cost__sum'] or 0
    hygiene_total = DairyHygiene.objects.filter(user=user).aggregate(Sum('cost'))['cost__sum'] or 0
    salaries_total = Salaries.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    feeds_total = Feeds.objects.filter(user=user).aggregate(Sum('cost'))['cost__sum'] or 0
    equipment_total = DairyEquipment.objects.filter(user=user).aggregate(Sum('cost'))['cost__sum'] or 0
    drugs_total = VeterinaryDrugs.objects.filter(user=user).aggregate(Sum('cost'))['cost__sum'] or 0
    minerals_total = Minerals.objects.filter(user=user).aggregate(Sum('cost'))['cost__sum'] or 0
    insurance_total = LivestockInsurance.objects.filter(user=user).aggregate(Sum('total'))['total__sum'] or 0
    other_total = OtherExpense.objects.filter(user=user).aggregate(Sum('cost'))['cost__sum'] or 0
    

    total_for_all_expenses = (
        vet_bills_total + archaricides_total + hygiene_total + salaries_total +
        feeds_total + equipment_total + drugs_total + minerals_total + insurance_total + other_total
    )

    return Response({
        'vet_bills': list(vet_bills),
        'archaricides': list(archaricides),
        'hygiene': list(hygiene),
        'salaries': list(salaries),
        'feeds': list(feeds),
        'equipment': list(equipment),
        'drugs': list(drugs),
        'minerals': list(minerals),
        'insurance': list(insurance),
        'other': list(other),
        'calving':calving,
        'total_for_all_expenses': total_for_all_expenses,
    })
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

class FilteredMilkRecordsView(View):
    def get(self, request):
        user = request.user
        cow_id = request.GET.get('cow_id')
        period = request.GET.get('period', 'all')
        date_from = request.GET.get('from')
        date_to = request.GET.get('to')

        # Base filters
        filters = {'user': user}
        if cow_id and cow_id != 'all':
            filters['cow_name_id'] = cow_id

        # Choose the correct model and date field
        if period == 'daily':
            model = DailyMilkRecord
            date_field = 'date'
        elif period == 'weekly' or period == 'two_weeks':
            model = WeeklyMilkRecord
            date_field = 'week_start_date'
        elif period == 'monthly' or period == 'yearly':
            model = MonthlyMilkRecord
            date_field = 'month'
        else:
            model = MilkRecord
            date_field = 'date'

        if date_from and date_to:
            filters[f'{date_field}__range'] = (date_from, date_to)

        records = model.objects.filter(**filters).values()
        return JsonResponse(list(records), safe=False)
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
def payments(request):
    return render(request, 'portals/farmer/payments.html', {})

class PaymentsCreate(generics.CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [Is_Farmer]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class PaymentsList(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Payments.objects.filter(user=self.request.user).order_by('-id')
    
class PaymentsUpdate(generics.UpdateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [Is_Farmer]
    
class PaymentsDelete(generics.DestroyAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

@user_passes_test(farmer_check, login_url='farmer-login')
def buyers(request):
    return render(request, 'portals/farmer/buyer.html', {})  # Your template


class BuyerCreate(generics.CreateAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    permission_classes = [Is_Farmer]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BuyerList(generics.ListAPIView):
    serializer_class = BuyerSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Buyer.objects.filter(user=self.request.user).order_by('-id')
    
@api_view(['GET'])
@permission_classes([Is_Farmer])
def get_buyers_by_category(request):
    category = request.GET.get('category')
    if category:
        buyers = Buyer.objects.filter(category=category, user=request.user)
    else:
        buyers = Buyer.objects.none()

    serializer = BuyerSerializer(buyers, many=True)
    return Response(serializer.data)

def buyers_by_category(request):
    category = request.GET.get('category')
    if category:
        buyers = Buyer.objects.filter(category=category)
        data = [{'id': b.id, 'name': b.name, 'category': b.category} for b in buyers]
    else:
        data = []
    return JsonResponse(data, safe=False)


class BuyerUpdate(generics.UpdateAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    permission_classes = [Is_Farmer]


class BuyerDelete(generics.DestroyAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    permission_classes = [Is_Farmer]

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
           
            return SampleCollection.objects.filter(user=user).order_by('-id')
        
        elif user.is_farmer:
            
            return SampleCollection.objects.filter(assigned_to=user).order_by('-id')

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
           
            return SampleProcessing.objects.filter(user=user).order_by('-id')
        
        elif user.is_farmer:
            
            return SampleProcessing.objects.filter(assigned_to=user).order_by('-id')

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
           
            return PostMortemRecord.objects.filter(user=user).order_by('-id')
        
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
def vaccination_official_view(request):
    return render(request, 'portals/reports/vaccination_official.html', {})
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsVetOrOfficial])
def vaccination_record_filter(request):
    try:
        user = request.user

        # 🧑‍⚕️ If vet officer: show records they assigned
        if getattr(user, 'is_vet_officer', False):
            records = VaccinationRecord.objects.filter(
                assigned_by=user
            ).annotate(
                assigned_to_username=F("assigned_to_official__username")
            ).values(
                "id", "date_of_vaccination", "species_targeted", "vaccination_of",
                "number_of_animals_vaccinated", "assigned_to_username"
            )
            return Response({
                "user_type": "vet_officer",
                "records": list(records),
            })

        # 🏛️ If official: show records assigned to them
        elif getattr(user, 'is_official', False):
            records = VaccinationRecord.objects.filter(
                assigned_to_official=user
            ).annotate(
                assigned_by_username=F("assigned_by__username")
            ).values(
                "id", "date_of_vaccination", "species_targeted", "vaccination_of",
                "number_of_animals_vaccinated", "assigned_by_username"
            )
            return Response({
                "user_type": "official",
                "records": list(records),
            })

        return Response({"error": "You do not have access to these records."}, status=403)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
class VaccinationRecordCreate(generics.CreateAPIView):
    queryset = VaccinationRecord.objects.all()
    serializer_class = VaccinationRecordSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class VaccinationRecordList(generics.ListAPIView):
    serializer_class = VaccinationRecordSerializer
    permission_classes = [Is_Vet|Is_Farmer | Is_Official]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
           
            return VaccinationRecord.objects.filter(user=user).order_by('-id')
        
        if user.is_official:
           
            return VaccinationRecord.objects.filter(assigned_to_official=user).order_by('-id')
        
        
        if user.is_farmer:
            
            return VaccinationRecord.objects.filter(assigned_to=user).order_by('-id')

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
            return ClinicalRecord.objects.filter(user=user).order_by('-id')

        elif user.is_farmer:
            # Farmers can view records assigned to them
            return ClinicalRecord.objects.filter(assigned_to=user).order_by('-id')

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
    permission_classes = [Is_Vet | Is_Official]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return DiseaseReport.objects.filter(user=user).order_by('-id')
        
        if user.is_official:
            return DiseaseReport.objects.filter(assigned_to_official=user).order_by('-id')

    
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

def slaughterhouse_view(request):
    return render(request, 'portals/reports/slaughter_official.html', {})

class SlaughterhouseCreate(generics.CreateAPIView):
    queryset = Slaughterhouse.objects.all()
    serializer_class = SlaughterhouseSerializer
    permission_classes = [Is_Vet | Is_Farmer | Is_Official]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SlaughterhouseList(generics.ListAPIView):
    serializer_class = SlaughterhouseSerializer
    permission_classes = [Is_Vet | Is_Farmer | Is_Official]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return Slaughterhouse.objects.filter(assigned_to_vet=user).order_by('-id')
        
        if user.is_official:
            return Slaughterhouse.objects.filter(assigned_to_official=user).order_by('-id')
        
        if user.is_farmer:
            return Slaughterhouse.objects.filter(user=user).order_by('-id')

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
def employee_view(request):
     return render(request, 'portals/reports/employee_view.html', {})
class EmployeeCreate(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [Is_Farmer]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EmployeeList(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [Is_Vet | Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return Employee.objects.filter(assigned_to_vet=user).order_by('-id')
        
        # if user.is_official:
        #     return Employee.objects.filter(assigned_to_official=user).order_by('-id')
        
        if user.is_farmer:
            return Employee.objects.filter(user=user).order_by('-id')

        return Employee.objects.none()

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
def butcher_view(request):
    return render(request, 'portals/reports/butcher_view.html', {})
class ButcherCreate(generics.CreateAPIView):
    queryset = Butcher.objects.all()
    serializer_class = ButcherSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ButcherList(generics.ListAPIView):
    serializer_class = ButcherSerializer
    permission_classes = [Is_Vet | Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return Butcher.objects.filter(user=user).order_by('-id').order_by('-id')
        
        elif user.is_farmer:
            return Butcher.objects.filter(user=user).order_by('-id').order_by('-id')

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
        serializer.save(user=self.request.user)

class InvoiceList(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [Is_Vet | Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            
            return Invoice.objects.filter(user=user).order_by('-id')
        
        elif user.is_farmer:
            
            return Invoice.objects.filter(assigned_to=user).order_by('-id')

        return Invoice.objects.none()

class InvoiceUpdate(generics.UpdateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [Is_Vet]

class InvoiceDelete(generics.DestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [Is_Vet]
    
   
def score(request):
    user=request.user
    score = Attempt.objects.filter(user=user)
    context = {
            'scores': score,
            
        }
    return render(request,'portals/reports/results.html',context)
 
@csrf_exempt
def start_quiz(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({'message': 'user_id is required'}, status=400)

        try:
            user = get_object_or_404(User, id=user_id)
            questions = get_random_questions_for_user(user)
            if not questions:
                return JsonResponse({'message': 'No questions available for your category'}, status=400)

            return JsonResponse({
                'questions': [{
                    'id': q.id,
                    'text': q.text,
                    'options': {'A': q.option_a, 'B': q.option_b, 'C': q.option_c, 'D': q.option_d}
                } for q in questions]
            })
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'Method not allowed'}, status=405)

@csrf_exempt
def submit_quiz(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            print(data)

            # Extract the user_id and answers
            user_id = data.get('user_id')
            answers = data.get('answers', {})

            # Get the user object or return a 404 if not found
            user = get_object_or_404(User, id=user_id)

            # Get or create the UserRetake object
            user_retake, created = UserRetake.objects.get_or_create(user=user)

            # Check if the user has any retakes left
            if user_retake.retakes_left < 1:
                return JsonResponse({'message': 'No retakes left', 'score': 0, 'retakes_left': 0}, status=400)

            score = 0
            # Process each question and its answer
            for question_id, answer in answers.items():
                question = get_object_or_404(Question, id=question_id)
                if question.correct_answer == answer:
                    score += 10

            # Save the attempt to the database
            attempt = Attempt.objects.create(user=user, score=score, attempt_number=4 - user_retake.retakes_left)

            # Check the score and respond accordingly
            if score >= 80:
                return JsonResponse({'message': 'Passed', 'score': score, 'retakes_left': user_retake.retakes_left})
            else:
                user_retake.retakes_left -= 1
                user_retake.save()
                return JsonResponse({'message': 'Failed', 'score': score, 'retakes_left': user_retake.retakes_left})

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)

        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'No attempts left'}, status=405)
def quiz_page(request):
    moderator = Moderator.objects.first() 
    return render(request, 'portals/reports/quiz.html', {'moderator': moderator})

    
# class QuestionListView(generics.ListAPIView):
#     permission_classes = [Is_Vet]
    
#     def get(self, request):
#         questions = Question.objects.all()
#         first_name = request.user.first_name.replace('%', '').strip()
#         last_name = request.user.last_name.replace('%', '').strip()
#         failed_attempts = QuestionResult.objects.filter(user=request.user, passed='fail').count()

#         # Determine if the submit button should be disabled (blurry)
#         disable_submit = failed_attempts >= 2

#         combined_name = f"{first_name} {last_name}"
#         context = {
#             'questions': questions,
#             'combined_name': combined_name,
#             'failed_attempts': failed_attempts,
#             'disable_submit': disable_submit  # Pass the flag to the template
#         }
#         return render(request, 'portals/reports/quiz.html', context)
    
def tutorial(request):
    return render(request, 'portals/reports/cpd.html', {})
def tutorialtest(request):
    return render(request, 'portals/reports/cpdtest.html', {})
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
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

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
    
def download_file(request, section_id):
    try:
        section = Section.objects.get(id=section_id)
        file_path = section.file.path  # Get the absolute file path
        
        # Verify that the file is in the 'media/uploads/' directory
        if os.path.exists(file_path) and 'media/uploads/' in file_path:
            # Serve the file as a downloadable response
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        else:
            raise Http404("File not found in the uploads directory")
    except Section.DoesNotExist:
        raise Http404("Section not found")
      
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
#cpd qustions 
class QuizView(View):
    permission_classes = [Is_Vet]
    
    def get(self, request, section_id):
        section = get_object_or_404(Section, id=section_id)
        questions = CpdQuestions.objects.filter(section=section)
        first_name = request.user.first_name.replace('%', '').strip()
        last_name = request.user.last_name.replace('%', '').strip()
        failed_attempts = QuizResult.objects.filter(user=request.user, section=section, passed='fail').count()

        # Determine if the submit button should be disabled (blurry)
        disable_submit = failed_attempts >= 2

        combined_name = f"{first_name} {last_name}"
        context = {
            'questions': questions,
            'section': section,
            'combined_name': combined_name,
            'failed_attempts': failed_attempts,
            'disable_submit': disable_submit  # Pass the flag to the template
        }
        return render(request, 'portals/reports/cpdquestions.html', context)
class QuizSubmit(View):
    permission_classes = [Is_Vet]

    def post(self, request, section_id):
        # Combine user's first and last name
        first_name = f"{request.user.first_name}"
        last_name = f"{request.user.last_name}"
        
        # Fetch the section instance or raise 404
        section = get_object_or_404(Section, id=section_id)
        
        # Ensure the quiz has a time limit (optional logic)
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(minutes=30)
        if timezone.now() > end_time:
            return JsonResponse({"error": "Time's up!"}, status=400)
        
        
        questions = CpdQuestions.objects.filter(section=section)
        total_questions = questions.count()
        
        if total_questions == 0:
            messages.error(request,"No questions available in this section")

        
        failed_attempts = QuizResult.objects.filter(user=request.user, section=section, passed='fail').count()
        
        if failed_attempts >= 2:
             messages.error(request,"You have already failed this quiz twice and can no longer retake it.")

      
        correct_count = 0
        for question in questions:
            question_id = str(question.id)
            selected_choice_id = request.POST.get(f'answers[{question_id}]')
            
            
            correct_choice = CpdChoices.objects.filter(question_id=question.id, is_correct=True).first()
            if correct_choice and str(correct_choice.id) == selected_choice_id:
                correct_count += 1
        
        
        score = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        passed_status = 'pass' if score >= 80 else 'fail'
        
        
        result = QuizResult.objects.create(
            user=request.user,
            section=section,  
            score=score,
            passed=passed_status, 
            failed_attempts=failed_attempts,
        )
        
        
        context = {
            'result': result,
            'score': score,
            'passed': passed_status,
            'section': section,
            'first_name': first_name,
            'last_name': last_name,
            'failed_attempts':failed_attempts,
        }
        
        if passed_status == 'fail':
            context['retake'] = True
        
        # Render the results page
        return render(request, 'portals/reports/cpdresult.html', context)

class QuestionCreateAPIView(generics.CreateAPIView):
    queryset = CpdQuestions.objects.all()
    serializer_class = CpdQuestionsSerializer
    permission_classes = [Is_Vet]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Question created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def result(request):
    return render(request,'portals/reports/myresults.html',{})




def generate_certificate(request, first_name, last_name):
    template_path = os.path.join(settings.STATIC_ROOT, "portals", "assets", "img", "certificate_1.png")
    template = cv2.imread(template_path)
    if template is None:
        return HttpResponse("Certificate template not found", status=500)

    registration_number = request.user.registration_number
    date = now()
    date_string = date.strftime('%d/%m/%Y')

    
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 2
    font_color = (0, 0, 255)
    thickness = 3

    
    canvas_width = template.shape[1]
    y_coordinate = 680
    spacing = 50  

   
    first_name_size = cv2.getTextSize(first_name, font, font_scale, thickness)[0]
    last_name_size = cv2.getTextSize(last_name, font, font_scale, thickness)[0]
    total_name_width = first_name_size[0] + spacing + last_name_size[0]

    if total_name_width <= canvas_width:
        first_name_coords = ((canvas_width - total_name_width) // 2, y_coordinate)
        last_name_coords = (first_name_coords[0] + first_name_size[0] + spacing, y_coordinate)
    else:
        
        first_name_coords = (100, y_coordinate)
        last_name_coords = (first_name_coords[0] + first_name_size[0] + spacing, y_coordinate)

    
    date_coords = (300, 950)
    signature_coords = (1200, 950)
    kvb_no_coords = (910, 760)

    
    cv2.putText(template, first_name, first_name_coords, font, font_scale, font_color, thickness, cv2.LINE_AA)
    cv2.putText(template, last_name, last_name_coords, font, font_scale, font_color, thickness, cv2.LINE_AA)

    
    cv2.putText(template, date_string, date_coords, font, 1, (0, 0, 0), 2, cv2.LINE_AA)

    
    #cv2.putText(template, "Authorized Signature", signature_coords, font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(template, registration_number, kvb_no_coords, font, 1, (0, 0, 0), 2, cv2.LINE_AA)

    
    success, buffer = cv2.imencode(".jpg", template)
    if not success:
        return HttpResponse("Error generating certificate", status=500)

    
    response = HttpResponse(buffer.tobytes(), content_type="image/jpeg")
    response["Content-Disposition"] = f'attachment; filename="{first_name}_certificate.jpg"'

    return response



class QuizResultList(generics.ListAPIView):
    serializer_class = QuizResultSerializer
    permission_classes = [Is_Vet]
    
    def get_queryset(self):
        return QuizResult.objects.all()
    
def livestock_examination(request):
    return render(request, 'portals/reports/examination.html', {})
def livestock_examination_view(request):
    return render(request, 'portals/reports/examination_view.html', {})

# Create View
class LivestockExaminationCreate(generics.CreateAPIView):
    queryset = LivestockExaminationRecord.objects.all()
    serializer_class = LivestockExaminationRecordSerializer
    permission_classes = [Is_Farmer | Is_Vet]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
# List View
class LivestockExaminationList(generics.ListAPIView):
    serializer_class = LivestockExaminationRecordSerializer
    permission_classes = [Is_Farmer | Is_Vet]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return LivestockExaminationRecord.objects.filter(user=user).order_by('-id')

# Update View
class LivestockExaminationUpdate(generics.UpdateAPIView):
    queryset = LivestockExaminationRecord.objects.all()
    serializer_class = LivestockExaminationRecordSerializer
    permission_classes = [Is_Farmer | Is_Vet]

# Delete View
class LivestockExaminationDelete(generics.DestroyAPIView):
    queryset = LivestockExaminationRecord.objects.all()
    serializer_class = LivestockExaminationRecordSerializer
    permission_classes = [Is_Farmer | Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
            
def calving_record(request):
    return render(request, 'portals/reports/calving_records.html', {})

# Create View
class CalvingRecordCreate(generics.CreateAPIView):
    queryset = CalvingRecord.objects.all()
    serializer_class = CalvingRecordSerializer
    permission_classes = [Is_Farmer]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
# List View
class CalvingRecordList(generics.ListAPIView):
    serializer_class = CalvingRecordSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return CalvingRecord.objects.filter(user=user).order_by('-id')

# Update View
class CalvingRecordUpdate(generics.UpdateAPIView):
    queryset = CalvingRecord.objects.all()
    serializer_class = CalvingRecordSerializer
    permission_classes = [Is_Farmer]

# Delete View
class CalvingRecordDelete(generics.DestroyAPIView):
    queryset = CalvingRecord.objects.all()
    serializer_class = CalvingRecordSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
    
def assessment_record(request):
    return render(request, 'portals/reports/assessment.html', {})
def assessment_record_view(request):
    return render(request, 'portals/reports/assessment_official.html', {})

# Create View
class AssessmentRecordCreate(generics.CreateAPIView):
    queryset = AssessmentRecord.objects.all()
    serializer_class = AssessmentRecordSerializer
    permission_classes = [Is_Farmer | Is_Vet ]  

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

# List View
class AssessmentRecordList(generics.ListAPIView):
    serializer_class = AssessmentRecordSerializer
    permission_classes = [Is_Farmer | Is_Vet |Is_Official]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return AssessmentRecord.objects.filter(user=user).order_by('-id')
        if user.is_farmer:
                return AssessmentRecord.objects.filter(assigned_to=user).order_by('-id')

        return AssessmentRecord.objects.none()
# Update View
class AssessmentRecordUpdate(generics.UpdateAPIView):
    queryset = AssessmentRecord.objects.all()
    serializer_class = AssessmentRecordSerializer
    permission_classes = [Is_Farmer | Is_Vet]

# Delete View
class AssessmentRecordDelete(generics.DestroyAPIView):
    queryset = AssessmentRecord.objects.all()
    serializer_class = AssessmentRecordSerializer
    permission_classes = [Is_Farmer | Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
        
def daily_kill_report(request):
    return render(request, 'portals/reports/kills.html', {})
def daily_kill_report_view(request):
    return render(request, 'portals/reports/kills_official.html', {})

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsVetOrOfficial])
def daily_kill_filter(request):
    try:
        user = request.user

        # 🧑‍⚕️ If vet officer: show records they assigned
        if getattr(user, 'is_vet_officer', False):
            records = DailyKill.objects.filter(
                assigned_by=user
            ).annotate(
                assigned_to_username=F("assigned_to_official__username")
            ).values(
                "id", "date", "livestock_category", "total_kills_per_day", "assigned_to_username"
            )
            return Response({
                "user_type": "vet_officer",
                "records": list(records),
            })

        # 🏛️ If official: show records assigned to them
        elif getattr(user, 'is_official', False):
            records = DailyKill.objects.filter(
                assigned_to_official=user
            ).annotate(
                assigned_by_username=F("assigned_by__username")
            ).values(
                "id", "date", "livestock_category", "total_kills_per_day", "assigned_by_username"
            )
            return Response({
                "user_type": "official",
                "records": list(records),
            })

        return Response({"error": "You do not have access to these records."}, status=403)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

class DailyKillCreate(generics.CreateAPIView):
    queryset = DailyKill.objects.all()
    serializer_class = DailyKillSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        user = self.request.user
        assigned_to_official = self.request.data.get("assigned_to_official")

        if assigned_to_official:
            serializer.save(user=user, assigned_by=user)  # Assign `assigned_by` if an official is assigned
        else:
            serializer.save(user=user)

class DailyKillList(generics.ListAPIView):
    serializer_class = DailyKillSerializer
    permission_classes = [Is_Vet | Is_Official]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        user_filter = self.request.query_params.get("user", None)  # Get user filter from query params

        if user_filter and user_filter.lower() == "all":
            return DailyKill.objects.all().order_by('-id')  # Retrieve all records

        if user.is_vet_officer:
            return DailyKill.objects.filter(user=user).order_by('-id')
        
        if user.is_farmer:
            return DailyKill.objects.filter(assigned_to_farmer=user).order_by('-id')


        if user.is_official:
            return DailyKill.objects.filter(assigned_to_official=user).order_by('-id')

        return DailyKill.objects.none()
class DailyKillUpdate(generics.UpdateAPIView):
    queryset = DailyKill.objects.all()
    serializer_class = DailyKillSerializer
    permission_classes = [Is_Vet]

class DailyKillDelete(generics.DestroyAPIView):
    queryset = DailyKill.objects.all()
    serializer_class = DailyKillSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
        
def movement_permit_report(request):
    return render(request, 'portals/reports/movement.html', {})
def movement_permit_report_view(request):
    return render(request, 'portals/reports/movement_view.html', {})

class MovementPermitCreate(generics.CreateAPIView):
    queryset = MovementPermit.objects.all()
    serializer_class = MovementPermitSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    permission_classes = [Is_Vet]
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class MovementPermitList(generics.ListAPIView):
    serializer_class = MovementPermitSerializer
    permission_classes = [Is_Vet | Is_Official]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return MovementPermit.objects.filter(user=user).order_by('-id')
        if user.is_official:
            return MovementPermit.objects.filter(assigned_to_official=user).order_by('-id')

        return MovementPermit.objects.none()

    def stream_file(self, request, permit_id):
        # Get the movement permit object based on the ID
        try:
            permit = MovementPermit.objects.get(id=permit_id)
        except MovementPermit.DoesNotExist:
            return HttpResponseNotFound("Movement Permit not found.")

        # Assuming `uploaded_report` is the file field on MovementPermit model
        file_path = permit.uploaded_permit.path

        # Check if the file exists
        if not os.path.exists(file_path):
            return HttpResponseNotFound("File not found.")

        # Open the file and stream it
        file = open(file_path, 'rb')
        response = FileResponse(file, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{permit.uploaded_permit.name}"'
        return response

class MovementPermitUpdate(generics.UpdateAPIView):
    queryset = MovementPermit.objects.all()
    serializer_class = MovementPermitSerializer
    permission_classes = [Is_Vet]

class MovementPermitDelete(generics.DestroyAPIView):
    queryset = MovementPermit.objects.all()
    serializer_class = MovementPermitSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

# No Objection Views

def no_objection_report(request):
    return render(request, 'portals/reports/no_objection.html', {})

def no_objection_report_view(request):
    return render(request, 'portals/reports/no_objection_view.html', {})


class NoObjectionCreate(generics.CreateAPIView):
    queryset = NoObjection.objects.all()
    serializer_class = NoObjectionSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
class NoObjectionList(generics.ListAPIView):
    serializer_class = NoObjectionSerializer
    permission_classes = [Is_Vet |Is_Official]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return NoObjection.objects.filter(user=user)
        if user.is_official:
            return NoObjection.objects.filter(assigned_to_official=user)

        return NoObjection.objects.none()
class NoObjectionUpdate(generics.UpdateAPIView):
    queryset = NoObjection.objects.all()
    serializer_class = NoObjectionSerializer
    permission_classes = [Is_Vet|Is_Official]

class NoObjectionDelete(generics.DestroyAPIView):
    queryset = NoObjection.objects.all()
    serializer_class = NoObjectionSerializer
    permission_classes = [Is_Vet|Is_Official]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

# Monthly Report Views

def monthly_report(request):
    return render(request, 'portals/reports/monthly_report.html', {})

def monthly_report_view(request):
    return render(request, 'portals/reports/monthly_report_official.html', {})


class MonthlyReportCreate(generics.CreateAPIView):
    queryset = MonthlyReport.objects.all()
    serializer_class = MonthlyReportSerializer
    permission_classes = [Is_Vet |Is_Official]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class MonthlyReportList(generics.ListAPIView):
    serializer_class = MonthlyReportSerializer
    permission_classes = [Is_Vet |Is_Official]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return MonthlyReport.objects.filter(user=user).order_by('-id')
        if user.is_official:
            return MonthlyReport.objects.filter(assigned_to_official=user).order_by('-id')

        return MonthlyReport.objects.none()
class MonthlyReportUpdate(generics.UpdateAPIView):
    queryset = MonthlyReport.objects.all()
    serializer_class = MonthlyReportSerializer
    permission_classes = [Is_Vet |Is_Official]

class MonthlyReportDelete(generics.DestroyAPIView):
    queryset = MonthlyReport.objects.all()
    serializer_class = MonthlyReportSerializer
    permission_classes = [Is_Vet |Is_Official]

    def perform_destroy(self, instance):
        instance.delete()
def quarterly_report(request):
    return render(request, 'portals/reports/quarterly_report.html', {})

def quarterly_report_view(request):
    return render(request, 'portals/reports/quarterly_report_official.html', {})
        
class QuarterlyReportCreate(generics.CreateAPIView):
    queryset = QuarterlyReport.objects.all()
    serializer_class = QuarterlyReportSerializer
    permission_classes = [Is_Vet | Is_Official]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class QuarterlyReportList(generics.ListAPIView):
    serializer_class = QuarterlyReportSerializer
    permission_classes = [Is_Vet | Is_Official]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return  QuarterlyReport.objects.filter(user=user).order_by('-id')
        if user.is_official:
            return QuarterlyReport.objects.filter(assigned_to_official=user).order_by('-id')

        return QuarterlyReport.objects.none()
class QuarterlyReportUpdate(generics.UpdateAPIView):
    queryset = QuarterlyReport.objects.all()
    serializer_class = QuarterlyReportSerializer
    permission_classes = [Is_Vet | Is_Official]

class QuarterlyReportDelete(generics.DestroyAPIView):
    queryset = QuarterlyReport.objects.all()
    serializer_class = QuarterlyReportSerializer
    permission_classes = [Is_Vet | Is_Official]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

# Yearly Report Views
def yearly_report(request):
    return render(request, 'portals/reports/yearly_report.html', {})

def yearly_report_view(request):
    return render(request, 'portals/reports/yearly_report_official.html', {})

# Yearly Report Views
class YearlyReportCreate(generics.CreateAPIView):
    queryset = YearlyReport.objects.all()
    serializer_class = YearlyReportSerializer
    permission_classes = [Is_Vet | Is_Official]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class YearlyReportList(generics.ListAPIView):
    serializer_class = YearlyReportSerializer
    permission_classes = [Is_Vet | Is_Official]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return YearlyReport.objects.filter(user=user).order_by('-id')
        if user.is_official:
            return YearlyReport.objects.filter(assigned_to_official=user).order_by('-id')

        return YearlyReport.objects.none()
class YearlyReportUpdate(generics.UpdateAPIView):
    queryset = YearlyReport.objects.all()
    serializer_class = YearlyReportSerializer
    permission_classes = [Is_Vet | Is_Official]

class YearlyReportDelete(generics.DestroyAPIView):
    queryset = YearlyReport.objects.all()
    serializer_class = YearlyReportSerializer
    permission_classes = [Is_Vet | Is_Official]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
 
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsVetOrOfficial])
def prac_record_filter(request):
    try:
        user = request.user

        # 🧑‍⚕️ Vet officer: show records they assigned
        if getattr(user, 'is_vet_officer', False):
            records = Practitioner.objects.filter(
                assigned_by=user
            ).annotate(
                assigned_to_username=F("assigned_to_official__username")
            ).values(
                "id", "reg_date", "subcounty", "vet_category", "assigned_to_username"
            )
            return Response({
                "user_type": "vet_officer",
                "records": list(records),
            })

        # 🏛️ Government official: show records assigned to them
        elif getattr(user, 'is_official', False):
            records = Practitioner.objects.filter(
                assigned_to_official=user
            ).annotate(
                assigned_by_username=F("assigned_by__username")
            ).values(
                "id", "reg_date", "subcounty", "vet_category", "assigned_by_username"
            )
            return Response({
                "user_type": "official",
                "records": list(records),
            })

        return Response({"error": "You do not have access to these records."}, status=403)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
        
def practitioner_record(request):
    return render(request, 'portals/reports/practitioner.html', {})

def practitioner_record_view(request):
    return render(request, 'portals/reports/practitioner_official.html', {})

class PractitionerCreate(generics.CreateAPIView):
    queryset = Practitioner.objects.all()
    serializer_class = PractitionerSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class PractitionerList(generics.ListAPIView):
    serializer_class = PractitionerSerializer
    permission_classes = [Is_Vet | Is_Official]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return Practitioner.objects.filter(user=user).order_by('-county')
        if user.is_official:
            return Practitioner.objects.filter(assigned_to_official=user)

        return Practitioner.objects.none()

class PractitionerUpdate(generics.UpdateAPIView):
    queryset = Practitioner.objects.all()
    serializer_class = PractitionerSerializer
    permission_classes = [Is_Farmer | Is_Vet]

class PractitionerDelete(generics.DestroyAPIView):
    queryset = Practitioner.objects.all()
    serializer_class = PractitionerSerializer
    permission_classes = [Is_Farmer | Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
        
def irrigation(request):
    return render(request, 'portals/reports/irrigation.html', {})

def irrigation_view(request):
    return render(request, 'portals/reports/irrigation_view.html', {})
class UterineIrrigationCreate(generics.CreateAPIView):
    queryset = UterineIrrigationRecord.objects.all()
    serializer_class = UterineIrrigationRecordSerializer
    permission_classes = [Is_Vet | Is_Farmer]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)  


class UterineIrrigationList(generics.ListAPIView):
    serializer_class = UterineIrrigationRecordSerializer
    permission_classes = [Is_Vet | Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        
        if  user.is_vet_officer:
            return UterineIrrigationRecord.objects.filter(user=user).order_by('-id')
        if  user.is_farmer:
            return UterineIrrigationRecord.objects.filter(assigned_to=user).order_by('-id')

        return UterineIrrigationRecord.objects.none()


class UterineIrrigationUpdate(generics.UpdateAPIView):
    queryset = UterineIrrigationRecord.objects.all()
    serializer_class = UterineIrrigationRecordSerializer
    permission_classes = [Is_Vet | Is_Farmer]


class UterineIrrigationDelete(generics.DestroyAPIView):
    queryset = UterineIrrigationRecord.objects.all()
    serializer_class = UterineIrrigationRecordSerializer
    permission_classes = [Is_Vet | Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
        
        
def emergency_care(request):
    return render(request, 'portals/reports/emergency_care.html', {})

def emergency_care_view(request):
    return render(request, 'portals/reports/emergency_care_view.html', {})

class EmergencyCareCreate(generics.CreateAPIView):
    queryset = EmergencyCare.objects.all()
    serializer_class = EmergencyCareSerializer
    permission_classes = [Is_Vet | Is_Farmer]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class EmergencyCareList(generics.ListAPIView):
    serializer_class = EmergencyCareSerializer
    permission_classes = [Is_Vet | Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return EmergencyCare.objects.filter(user=user).order_by('-id')
        if user.is_farmer:
            return EmergencyCare.objects.filter(assigned_to=user).order_by('-id')

        return EmergencyCare.objects.none()

class EmergencyCareUpdate(generics.UpdateAPIView):
    queryset = EmergencyCare.objects.all()
    serializer_class = EmergencyCareSerializer
    permission_classes = [Is_Vet | Is_Farmer]

class EmergencyCareDelete(generics.DestroyAPIView):
    queryset = EmergencyCare.objects.all()
    serializer_class = EmergencyCareSerializer
    permission_classes = [Is_Vet | Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
        

# PriceList Views
def price_list(request):
    return render(request, 'portals/reports/price_list.html', {})

def price_list_view(request):
    return render(request, 'portals/reports/price_list_view.html', {})

class PriceListCreate(generics.CreateAPIView):
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    permission_classes = [Is_Farmer | Is_Vet]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class PriceListList(generics.ListAPIView):
    serializer_class = PriceListSerializer
    permission_classes = [Is_Farmer | Is_Vet]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return PriceList.objects.filter(user=user).order_by('-id')

class PriceListUpdate(generics.UpdateAPIView):
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    permission_classes = [Is_Farmer | Is_Vet]

class PriceListDelete(generics.DestroyAPIView):
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    permission_classes = [Is_Farmer | Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

# Supplier Views
def supplier(request):
    return render(request, 'portals/reports/supplier.html', {})

def supplier_view(request):
    return render(request, 'portals/reports/supplier_view.html', {})

class SupplierCreate(generics.CreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [Is_Farmer | Is_Vet]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class SupplierList(generics.ListAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [Is_Farmer | Is_Vet]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return Supplier.objects.filter(user=user).order_by('-id')

class SupplierUpdate(generics.UpdateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [Is_Farmer | Is_Vet]

class SupplierDelete(generics.DestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [Is_Farmer | Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

# Client Views
def client(request):
    return render(request, 'portals/reports/customer.html', {})

def client_view(request):
    return render(request, 'portals/reports/client_view.html', {})

class CustomerCreate(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [Is_Farmer | Is_Vet]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class CustomerList(generics.ListAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [Is_Farmer | Is_Vet]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return Customer.objects.filter(user=user).order_by('-id')

class CustomerUpdate(generics.UpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [Is_Farmer | Is_Vet]

class CustomerDelete(generics.DestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [Is_Farmer | Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

# Creditor Views
def creditor(request):
    return render(request, 'portals/reports/creditor.html', {})

def creditor_view(request):
    return render(request, 'portals/reports/creditor_view.html', {})

class CreditorCreate(generics.CreateAPIView):
    queryset = Creditor.objects.all()
    serializer_class = CreditorSerializer
    permission_classes = [Is_Farmer | Is_Vet]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class CreditorList(generics.ListAPIView):
    serializer_class = CreditorSerializer
    permission_classes = [Is_Farmer | Is_Vet]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return Creditor.objects.filter(user=user).order_by('-id')

class CreditorUpdate(generics.UpdateAPIView):
    queryset = Creditor.objects.all()
    serializer_class = CreditorSerializer
    permission_classes = [Is_Farmer | Is_Vet]

class CreditorDelete(generics.DestroyAPIView):
    queryset = Creditor.objects.all()
    serializer_class = CreditorSerializer
    permission_classes = [Is_Farmer | Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

# Debtor Views
def debtor(request):
    return render(request, 'portals/reports/debtor.html', {})

def debtor_view(request):
    return render(request, 'portals/reports/debtor_view.html', {})

class DebtorCreate(generics.CreateAPIView):
    queryset = Debtor.objects.all()
    serializer_class = DebtorSerializer
    permission_classes = [Is_Farmer | Is_Vet]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class DebtorList(generics.ListAPIView):
    serializer_class = DebtorSerializer
    permission_classes = [Is_Farmer | Is_Vet]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return Debtor.objects.filter(user=user).order_by('-id')

class DebtorUpdate(generics.UpdateAPIView):
    queryset = Debtor.objects.all()
    serializer_class = DebtorSerializer
    permission_classes = [Is_Farmer | Is_Vet]

class DebtorDelete(generics.DestroyAPIView):
    queryset = Debtor.objects.all()
    serializer_class = DebtorSerializer
    permission_classes = [Is_Farmer | Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
            
def client_request(request):
    return render(request, 'portals/reports/request.html', {})

def client_request_view(request):
    return render(request, 'portals/reports/request_view.html', {})

@csrf_exempt
def update_request_status(request):
    if request.method == "POST":
        request_id = request.POST.get("request_id")
        new_status = request.POST.get("status")

        if not request_id or not new_status:
            return JsonResponse({"success": False, "error": "Missing data"}, status=400)

        try:
            client_request = ClientRequest.objects.get(id=request_id)
            client_request.status = new_status
            client_request.save()
            return JsonResponse({"success": True, "status": new_status})

        except ClientRequest.DoesNotExist:
            return JsonResponse({"success": False, "error": "Request not found"}, status=404)

    elif request.method == "GET":
        requests = ClientRequest.objects.values("id", "status","judgement")
        return JsonResponse({"success": True, "requests": list(requests)})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


class ClientRequestCreate(generics.CreateAPIView):
    queryset = ClientRequest.objects.all()
    serializer_class = ClientRequestSerializer
    permission_classes = [Is_Farmer | Is_Vet]
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class ClientRequestList(generics.ListAPIView):
    serializer_class = ClientRequestSerializer
    permission_classes = [Is_Farmer | Is_Vet]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_farmer:
            return ClientRequest.objects.filter(user=user).order_by('-id')
       
        if user.is_vet_officer:
            return ClientRequest.objects.filter(assigned_to=user).order_by('-id')



class ClientRequestUpdate(generics.UpdateAPIView):
    queryset = ClientRequest.objects.all()
    serializer_class = ClientRequestSerializer
    permission_classes = [Is_Farmer | Is_Vet]

class ClientRequestDelete(generics.DestroyAPIView):
    queryset = ClientRequest.objects.all()
    serializer_class = ClientRequestSerializer
    permission_classes = [Is_Farmer | Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()


def vet_judgment(request):
    return render(request, 'portals/reports/judgement.html', {})

def vet_judgment_view(request):
    return render(request, 'portals/reports/judgement_view.html', {})


class VetJudgmentCreate(generics.CreateAPIView):
    serializer_class = VetJudgmentSerializer
    permission_classes = [Is_Vet | Is_Farmer]
    queryset = VetJudgment.objects.all()
    
    def perform_create(self, serializer):
        user = self.request.user
        vet_judgment = serializer.save(user=user)  # Save VetJudgment first
        
        client_request_id = self.request.data.get("client_request_id")
        
        if client_request_id:
            try:
                client_request = ClientRequest.objects.get(id=client_request_id)
                print("Before updating judgment:", client_request.judgement)  # Print before update
                
                client_request.judgement = True
                client_request.save()
                #client_request.refresh_from_db()# Save updated ClientRequest
                
                print("After updating judgment:", client_request.judgement)  # Print after update
            except ClientRequest.DoesNotExist:
                raise serializers.ValidationError({"client_request_id": "ClientRequest not found."}) 
              
class VetJudgmentList(generics.ListAPIView):
    serializer_class = VetJudgmentSerializer
    permission_classes = [Is_Vet | Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        if user.is_vet_officer:
            return VetJudgment.objects.filter(user=user).order_by('-id')
       
        if user.is_farmer:
            return VetJudgment.objects.filter(assigned_to=user).order_by('-id')


class VetJudgmentUpdate(generics.UpdateAPIView):
    queryset = VetJudgment.objects.all()
    serializer_class = VetJudgmentSerializer
    permission_classes = [Is_Vet]

class VetJudgmentDelete(generics.DestroyAPIView):
    queryset = VetJudgment.objects.all()
    serializer_class = VetJudgmentSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
  
def payment(request, lesson_id):
    return render(request, 'portals/reports/payment.html', {'lesson_id': lesson_id})         
def format_phone_number(phone):
    if phone.startswith("0"):
        return "254" + phone[1:]
    return phone

#payment  
@csrf_exempt      
def initiate_mpesa_payment(request):
    """Send an STK Push request to M-Pesa Express"""
    
    # Extract lesson_id from request (GET or POST)
    lesson_id = request.GET.get("lesson_id") or request.POST.get("lesson_id")

    if not lesson_id:
        return JsonResponse({"error": "Missing lesson_id"}, status=400)

    try:
        # Fetch lesson details
        lesson = Tutorial.objects.get(id=lesson_id)
        amount = float(lesson.unit_price)  # Assuming there's a price field
    except Tutorial.DoesNotExist:
        return JsonResponse({"error": "Lesson not found"}, status=404)

    # Get phone number
    phone_number = request.user.phone_number
    phone_number = format_phone_number(phone_number)

    # Generate Timestamp & Password
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(f"{MPESA_SHORTCODE}{MPESA_PASSKEY}{timestamp}".encode()).decode()

    # Get Access Token
    access_token = get_mpesa_access_token()
    if not access_token:
        return JsonResponse({"error": "Failed to get M-Pesa access token"}, status=400)

    # Prepare STK Push Request Payload
    payload = {
        "BusinessShortCode": MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": f"Lesson-{lesson_id}",
        "TransactionDesc": f"Payment for Lesson {lesson_id}"
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(MPESA_API_URL, json=payload, headers=headers)
    response_data = response.json()

    # Save initial payment request (before confirmation)
    if response_data.get("ResponseCode") == "0":
        Payment.objects.create(
            merchant_request_id=response_data["MerchantRequestID"],
            checkout_request_id=response_data["CheckoutRequestID"],
            amount=amount,
            phone_number=phone_number,
            lesson=lesson,  # Store lesson ID
            status="Pending"
        )

    return JsonResponse(response_data)

@csrf_exempt
def mpesa_callback(request):
    """Handle M-Pesa STK Push Callback"""
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            logger.info("Received M-Pesa Callback: %s", data)

            body = data.get("Body", {})
            stk_callback = body.get("stkCallback", {})

            result_code = stk_callback.get("ResultCode")
            checkout_request_id = stk_callback.get("CheckoutRequestID")

            print(f"Result Code: {result_code}, CheckoutRequestID: {checkout_request_id}")

            # Find the payment record
            payment = Payment.objects.filter(checkout_request_id=checkout_request_id).first()
            if not payment:
                print("Payment record not found for CheckoutRequestID: %s", checkout_request_id)
                return JsonResponse({"error": "Payment record not found"}, status=404)

            if result_code == 0:
                # Extract payment details
                callback_metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
                amount = next((item["Value"] for item in callback_metadata if item["Name"] == "Amount"), None)
                mpesa_receipt = next((item["Value"] for item in callback_metadata if item["Name"] == "MpesaReceiptNumber"), None)
                phone_number = next((item["Value"] for item in callback_metadata if item["Name"] == "PhoneNumber"), None)

                print(f"Payment Successful - Amount: {amount}, Receipt: {mpesa_receipt}, Phone: {phone_number}")

                # Check if receipt already exists
                if Payment.objects.filter(mpesa_receipt=mpesa_receipt).exists():
                    logger.warning(f"Duplicate MpesaReceiptNumber: {mpesa_receipt}")
                    return JsonResponse({"error": "Duplicate Mpesa receipt"}, status=400)

                # Update payment record
                payment.mpesa_receipt = mpesa_receipt
                payment.status = "Completed"
                payment.save()

                # Mark lesson as paid if it exists
                if payment.lesson:
                    payment.lesson.is_paid = True  # Ensure Lesson model has is_paid field
                    payment.lesson.save()
                    print(f"Lesson '{payment.lesson.id}' marked as paid.")

                return JsonResponse({"message": "Payment received successfully"}, status=200)

            else:
                logger.error(f"Payment Failed - Result Code: {result_code}")

                # Update Payment Status
                payment.status = "Failed"
                payment.save()

                return JsonResponse({"message": "Payment failed", "ResultCode": result_code}, status=400)

        except Exception as e:
            logger.error("Error processing callback: %s", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request"}, status=400)
@csrf_exempt
def check_mpesa_status(request):
    """Check M-Pesa payment status via AJAX polling."""
    if request.method == "POST":
        checkout_request_id = request.POST.get("checkout_request_id")

        # Get payment record
        payment = Payment.objects.filter(checkout_request_id=checkout_request_id).first()

        if payment:
            return JsonResponse({"status": payment.status}, status=200)
        return JsonResponse({"error": "Payment not found"}, status=404)

    return JsonResponse({"message": "Invalid request"}, status=400)

def management_committee(request):
    return render(request, 'portals/farmer/management_committee.html', {})

# Create View
class ManagementCommitteeCreate(generics.CreateAPIView):
    queryset = ManagementCommittee.objects.all()
    serializer_class = ManagementCommitteeSerializer
    permission_classes = [Is_Farmer]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

# List View
class ManagementCommitteeList(generics.ListAPIView):
    serializer_class = ManagementCommitteeSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return ManagementCommittee.objects.filter(user=user).order_by('-id')

# Update View
class ManagementCommitteeUpdate(generics.UpdateAPIView):
    queryset = ManagementCommittee.objects.all()
    serializer_class = ManagementCommitteeSerializer
    permission_classes = [Is_Farmer]

# Delete View
class ManagementCommitteeDelete(generics.DestroyAPIView):
    queryset = ManagementCommittee.objects.all()
    serializer_class = ManagementCommitteeSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()


# -------------------------------------------
# Hides and Skins Record Views
# -------------------------------------------

def hides_and_skins_record(request):
    return render(request, 'portals/farmer/hides_skins.html', {})

# Create View
class HidesAndSkinsRecordCreate(generics.CreateAPIView):
    queryset = HidesAndSkinsRecord.objects.all()
    serializer_class = HidesAndSkinsRecordSerializer
    permission_classes = [Is_Farmer]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

# List View
class HidesAndSkinsRecordList(generics.ListAPIView):
    serializer_class = HidesAndSkinsRecordSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return HidesAndSkinsRecord.objects.filter(user=user).order_by('-id')

# Update View
class HidesAndSkinsRecordUpdate(generics.UpdateAPIView):
    queryset = HidesAndSkinsRecord.objects.all()
    serializer_class = HidesAndSkinsRecordSerializer
    permission_classes = [Is_Farmer]

# Delete View
class HidesAndSkinsRecordDelete(generics.DestroyAPIView):
    queryset = HidesAndSkinsRecord.objects.all()
    serializer_class = HidesAndSkinsRecordSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
def approved_dairy_farms(request):
    return render(request, 'portals/farmer/approved_farms.html', {})
def approved_dairy_view(request):
    return render(request, 'portals/farmer/approved_view.html', {})


# Create View
class ApprovedDairyFarmCreate(generics.CreateAPIView):
    queryset = ApprovedDairyFarm.objects.all()
    serializer_class = ApprovedDairyFarmSerializer
    permission_classes = [Is_Farmer]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

# List View
class ApprovedDairyFarmList(generics.ListAPIView):
    serializer_class = ApprovedDairyFarmSerializer
    permission_classes = [Is_Farmer | Is_Vet | Is_Official]
    pagination_class = CustomPagination

    def get_queryset(self):
        
        return ApprovedDairyFarm.objects.all().order_by('-id')

# Update View
class ApprovedDairyFarmUpdate(generics.UpdateAPIView):
    queryset = ApprovedDairyFarm.objects.all()
    serializer_class = ApprovedDairyFarmSerializer
    permission_classes = [Is_Farmer]

# Delete View
class ApprovedDairyFarmDelete(generics.DestroyAPIView):
    queryset = ApprovedDairyFarm.objects.all()
    serializer_class = ApprovedDairyFarmSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
            
def slaughterhouse_hygiene_page(request):
    return render(request, 'portals/farmer/slaughter_hygiene.html', {})

class SlaughterhouseHygieneCreate(generics.CreateAPIView):
    queryset = SlaughterhouseHygiene.objects.all()
    serializer_class = SlaughterhouseHygieneSerializer
    permission_classes = [Is_Farmer]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SlaughterhouseHygieneList(generics.ListAPIView):
    serializer_class = SlaughterhouseHygieneSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        return SlaughterhouseHygiene.objects.filter(user=self.request.user).order_by('-id')

class SlaughterhouseHygieneUpdate(generics.UpdateAPIView):
    queryset = SlaughterhouseHygiene.objects.all()
    serializer_class = SlaughterhouseHygieneSerializer
    permission_classes = [Is_Farmer]

class SlaughterhouseHygieneDelete(generics.DestroyAPIView):
    queryset = SlaughterhouseHygiene.objects.all()
    serializer_class = SlaughterhouseHygieneSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

# =============================
# Slaughterhouse Asset Views
# =============================

def slaughterhouse_asset_page(request):
    return render(request, 'portals/farmer/slaughter_assets.html', {})

class SlaughterhouseAssetCreate(generics.CreateAPIView):
    queryset = SlaughterhouseAsset.objects.all()
    serializer_class = SlaughterhouseAssetSerializer
    permission_classes = [Is_Farmer]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SlaughterhouseAssetList(generics.ListAPIView):
    serializer_class = SlaughterhouseAssetSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        return SlaughterhouseAsset.objects.filter(user=self.request.user).order_by('-id')

class SlaughterhouseAssetUpdate(generics.UpdateAPIView):
    queryset = SlaughterhouseAsset.objects.all()
    serializer_class = SlaughterhouseAssetSerializer
    permission_classes = [Is_Farmer]

class SlaughterhouseAssetDelete(generics.DestroyAPIView):
    queryset = SlaughterhouseAsset.objects.all()
    serializer_class = SlaughterhouseAssetSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()         

def livestock_registration(request):
    return render(request, 'portals/reports/live_registration.html', {})
def livestock_data(request, livestock_type):
    records = LivestockRegistration.objects.filter(
        livestock_type=livestock_type
    ).order_by('-id').values()

    data = {
        "count": records.count(),
        "next": None,
        "previous": None,
        "results": list(records)
    }

    return JsonResponse(data, safe=False)
# Template render views
def dairy_cow_page(request):
    return render(request, 'portals/reports/dairy.html')

def beef_page(request):
    return render(request, 'portals/reports/beef.html')

def sheep_page(request):
    return render(request, 'portals/reports/sheep.html')

def goat_page(request):
    return render(request, 'portals/reports/goat.html')
class LivestockRegistrationCreate(generics.CreateAPIView):
    queryset = LivestockRegistration.objects.all()
    serializer_class = LivestockRegistrationSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class LivestockRegistrationList(generics.ListAPIView):
    serializer_class = LivestockRegistrationSerializer
    permission_classes = [Is_Vet]
    pagination_class = CustomPagination

    def get_queryset(self):
        return LivestockRegistration.objects.filter(user=self.request.user).order_by('-id')

class LivestockRegistrationUpdate(generics.UpdateAPIView):
    queryset = LivestockRegistration.objects.all()
    serializer_class = LivestockRegistrationSerializer
    permission_classes = [Is_Vet]

class LivestockRegistrationDelete(generics.DestroyAPIView):
    queryset = LivestockRegistration.objects.all()
    serializer_class = LivestockRegistrationSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
            
            
def eprescription(request):
    return render(request, 'portals/reports/eprescription.html', {})            
            
class VeterinaryEPrescriptionCreate(generics.CreateAPIView):
    queryset = VeterinaryEPrescription.objects.all()
    serializer_class = VeterinaryEPrescriptionSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class VeterinaryEPrescriptionList(generics.ListAPIView):
    serializer_class = VeterinaryEPrescriptionSerializer
    permission_classes = [Is_Vet]
    pagination_class = CustomPagination

    def get_queryset(self):
        return VeterinaryEPrescription.objects.filter(user=self.request.user).order_by('-id')


class VeterinaryEPrescriptionUpdate(generics.UpdateAPIView):
    queryset = VeterinaryEPrescription.objects.all()
    serializer_class = VeterinaryEPrescriptionSerializer
    permission_classes = [Is_Vet]


class VeterinaryEPrescriptionDelete(generics.DestroyAPIView):
    queryset = VeterinaryEPrescription.objects.all()
    serializer_class = VeterinaryEPrescriptionSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

def routine(request):
    return render(request, 'portals/reports/routine.html', {})
class RoutineManagementCreate(generics.CreateAPIView):
    queryset = RoutineManagement.objects.all()
    serializer_class = RoutineManagementSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class RoutineManagementList(generics.ListAPIView):
    serializer_class = RoutineManagementSerializer
    permission_classes = [Is_Vet]
    pagination_class = CustomPagination

    def get_queryset(self):
        return RoutineManagement.objects.filter(user=self.request.user).order_by('-id')


class RoutineManagementUpdate(generics.UpdateAPIView):
    queryset = RoutineManagement.objects.all()
    serializer_class = RoutineManagementSerializer
    permission_classes = [Is_Vet]


class RoutineManagementDelete(generics.DestroyAPIView):
    queryset = RoutineManagement.objects.all()
    serializer_class = RoutineManagementSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
            
            
            
def abortion(request):
    return render(request, 'portals/reports/abortion.html', {})            
class AbortionRecordCreate(generics.CreateAPIView):
    queryset = AbortionRecord.objects.all()
    serializer_class = AbortionRecordSerializer
    permission_classes = [Is_Vet]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class AbortionRecordList(generics.ListAPIView):
    serializer_class = AbortionRecordSerializer
    permission_classes = [Is_Vet]
    pagination_class = CustomPagination

    def get_queryset(self):
        return AbortionRecord.objects.filter(user=self.request.user).order_by('-id')


class AbortionRecordUpdate(generics.UpdateAPIView):
    queryset = AbortionRecord.objects.all()
    serializer_class = AbortionRecordSerializer
    permission_classes = [Is_Vet]


class AbortionRecordDelete(generics.DestroyAPIView):
    queryset = AbortionRecord.objects.all()
    serializer_class = AbortionRecordSerializer
    permission_classes = [Is_Vet]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()