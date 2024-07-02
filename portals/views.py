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
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Calf
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import CalfRegForm
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






def vet_check(request):
    return request.is_vet_officer

def farmer_check(request):
    return request.is_farmer

def student_check(request):
    return request.is_student    


@login_required
def portal_vet(request):
    vet_officers = Vet_Officer.objects.all()
    no_vet_forms =Vet_Forms.objects.filter(vet_username=request.user).count()
    context = {
        'all_vets': vet_officers,
        'count': no_vet_forms
    }
    return render(request, 'portals/dashboardVet.html', context)
    
    
    
    
def vet_list(request):
    vet_officers = Vet_Officer.objects.all()
    no_vet_forms =Vet_Forms.objects.filter(vet_username=request.user).count()
    context = {
        'all_vets': vet_officers,
        'count': no_vet_forms
    }
    return render(request, 'portals/vetList.html', context)
    

@login_required
def portal_farmer(request):
    vet_officers = Vet_Officer.objects.all()
    context = {
        'all_vets': vet_officers
    }
    return render(request, 'portals/dashboardFarmer.html', context)

@user_passes_test(student_check, login_url='vet-login')
def portal_student(request):
    vet_officers = Vet_Officer.objects.all()
    context = {
        'all_vets': vet_officers
    }
    return render(request, 'portals/dashboardStudent.html', context)  


@login_required
def sick_form_view(request):
    sick_approach_forms = Sick_Approach_Form.objects.filter(vet_form__vet_username=request.user)
    context = {
        'form_name': 'Clinical Approach Form',
        'forms': sick_approach_forms
    }    
    return render(request, 'portals/formview.html', context)
 
    
@login_required
def edit_sick_form(request, pk):
	try:
		sick_sel = Sick_Approach_Form.objects.get(pk = pk)
	except Sick_Approach_Form.DoesNotExist:
		return redirect('index')
	sick_form = SickApproachForm(request.POST or None, instance = sick_sel)
	if sick_form.is_valid():
		sick_form.save()
		return redirect('index')
	return render(request, 'portals/editform.html', {'form':sick_form, 'form_name':'Clinical'})


 
@login_required
def dead_form_view(request):
    dead_approach_forms = Death_Approach_Form.objects.filter(vet_form__vet_username=request.user)
    context = {
        'form_name': 'Post Mortem Approach Form',
        'forms': dead_approach_forms
    }    
    return render(request, 'portals/deadformview.html', context)
 

@login_required
def edit_dead_form(request, pk):
	try:
		dead_sel = Death_Approach_Form.objects.get(pk = pk)
	except Death_Approach_Form.DoesNotExist:
		return redirect('index')
	dead_form = DeathApproachForm(request.POST or None, instance = dead_sel)
	if dead_form.is_valid():
		dead_form.save()
		return redirect('index')
	return render(request, 'portals/editform.html', {'form':dead_form, 'form_name':'Post Mortem'})

 
@login_required
def surgical_form_view(request):
    surgical_approach_forms = Surgical_Approach_Form.objects.filter(vet_form__vet_username=request.user)
    context = {
        'form_name': 'surgical Approach Form',
        'forms': surgical_approach_forms
    }    
    return render(request, 'portals/surgicalformview.html', context)
 

@login_required
def edit_surgical_form(request, pk):
	try:
		surgical_sel = Surgical_Approach_Form.objects.get(pk = pk)
	except Surgical_Approach_Form.DoesNotExist:
		return redirect('index')
	surgical_form = SurgicalApproachForm(request.POST or None, instance = surgical_sel)
	if surgical_form.is_valid():
		surgical_form.save()
		return redirect('index')
	return render(request, 'portals/editform.html', {'form':surgical_form, 'form_name':'Surgical'})

@login_required
def deworming_form_view(request):
    deworming_approach_forms = Deworming_Form.objects.filter(vet_form__vet_username=request.user)
    context = {
        'form_name': 'Deworming Approach Form',
        'forms': deworming_approach_forms
    }    
    return render(request, 'portals/dewormingformview.html', context)
 

@login_required
def edit_deworming_form(request, pk):
	try:
		surgical_sel = Deworming_Form.objects.get(pk = pk)
	except Deworming_Form.DoesNotExist:
		return redirect('index')
	deworming_form = DewormingForm(request.POST or None, instance = surgical_sel)
	if deworming_form.is_valid():
		deworming_form.save()
		return redirect('index')
	return render(request, 'portals/editform.html', {'form':deworming_form, 'form_name':'Deworming'})


@login_required
def vaccination_form_view(request):
    vaccination_approach_forms = Vaccination_Form.objects.filter(vet_form__vet_username=request.user)
    context = {
        'form_name': 'Vaccination Form',
        'forms': vaccination_approach_forms
    }    
    return render(request, 'portals/vaccinationformview.html', context)
 

@login_required
def edit_vaccination_form(request, pk):
	try:
		surgical_sel = Vaccination_Form.objects.get(pk = pk)
	except Vaccination_Form.DoesNotExist:
		return redirect('index')
	vaccination_form = VaccinationForm(request.POST or None, instance = surgical_sel)
	if vaccination_form.is_valid():
		vaccination_form.save()
		return redirect('index')
	return render(request, 'portals/editform.html', {'form':vaccination_form, 'form_name':'Vaccination'})



@login_required
def artificial_form_view(request):
    artificial_approach_forms = Artificial_Insemination_Form.objects.filter(vet_form__vet_username=request.user)
    context = {
        'form_name': 'Artificial Form',
        'forms': artificial_approach_forms
    }    
    return render(request, 'portals/artificialformview.html', context)
 

@login_required
def edit_artificial_form(request, pk):
	try:
		surgical_sel = Artificial_Insemination_Form.objects.get(pk = pk)
	except Artificial_Form.DoesNotExist:
		return redirect('index')
	Artificial_form = ArtificialInseminationForm(request.POST or None, instance = surgical_sel)
	if Artificial_form.is_valid():
		artificial_form.save()
		return redirect('index')
	return render(request, 'portals/editform.html', {'form':artificial_form, 'form_name':'artificial'})




@login_required
def pregnancy_form_view(request):
    pregnancy_approach_forms = Pregnancy_Diagnosis_Form.objects.filter(vet_form__vet_username=request.user)
    context = {
        'form_name': 'Pregnancy diagnosis Form',
        'forms': pregnancy_approach_forms
    }    
    return render(request, 'portals/pregnancyformview.html', context)
 

@login_required
def edit_pregnancy_form(request, pk):
	try:
		surgical_sel = Pregnancy_Diagnosis_Form.objects.get(pk = pk)
	except Pregnancy_Diagnosis_Form.DoesNotExist:
		return redirect('index')
	pregnancy_form = PregnancyDiagnosisForm(request.POST or None, instance = surgical_sel)
	if pregnancy_form.is_valid():
		pregnancy_form.save()
		return redirect('index')
	return render(request, 'portals/editform.html', {'form':Pregnancy_Diagnosis_Form, 'form_name':'pregnancy'})




@login_required
def clinical_approach(request):
    return render(request, 'portals/clinical_approach.html') 

import json
@login_required
def sick_approach(request):
    if request.method == "POST":
        form = SickApproachForm(request.POST)
        if form.is_valid():
            # Create a new Vet_Forms instance with vet_username and is_sick_approach_form
            vet_sick_form = Vet_Forms(vet_username=request.user, is_sick_approach_form=True)
            vet_sick_form.save()

            # Associate the Vet_Forms instance with the SickApproachForm instance
            form_instance = form.save(commit=False)
            form_instance.vet_form = vet_sick_form
            form_instance.save()

            messages.success(request, 'Details successfully saved')
            return redirect('vet-portal')

    else:
        form = SickApproachForm()

    context = {
        'form': form,
        'name': 'Clinical Approach Form'
    }

    return render(request, 'portals/forms.html', context)

@login_required
def dead_approach(request):
    if request.method == "POST":
        form = DeathApproachForm(request.POST)
        if form.is_valid():
            # Create a new Vet_Forms instance with vet_username and is_dead_approach_form
            vet_death_form = Vet_Forms(vet_username=request.user, is_dead_approach_form=True)
            vet_death_form.save()

            # Associate the Vet_Forms instance with the DeathApproachForm instance
            form_instance = form.save(commit=False)
            form_instance.vet_form = vet_death_form
            form_instance.save()

            messages.success(request, 'Details successfully saved')
            return redirect('vet-portal')

    else:
        form = DeathApproachForm()

    context = {
        'form': form,
        'name': 'Post Mortem Approach Form'
    }

    return render(request, 'portals/forms.html', context) 

@login_required
def surgical_approach(request):
    if request.method == "POST":
        form = SurgicalApproachForm(request.POST)
        if form.is_valid():
            # Create a new Vet_Forms instance with vet_username and is_surgical_approach_form
            vet_surgical_form = Vet_Forms(vet_username=request.user, is_surgical_approach_form=True)
            vet_surgical_form.save()

            # Associate the Vet_Forms instance with the SurgicalApproachForm instance
            form_instance = form.save(commit=False)
            form_instance.vet_form = vet_surgical_form
            form_instance.save()

            messages.success(request, 'Details successfully saved')
            return redirect('vet-portal')

    else:
        form = SurgicalApproachForm()

    context = {
        'form': form,
        'name': 'Surgical Approach Form'
    }

    return render(request, 'portals/forms.html', context)

@login_required
def deworming(request):
    if request.method == "POST":
        form = DewormingForm(request.POST)
        if form.is_valid():
            # Create a new Vet_Forms instance with vet_username and is_deworming_form
            vet_deworming_form = Vet_Forms(vet_username=request.user, is_deworming_form=True)
            vet_deworming_form.save()

            # Associate the Vet_Forms instance with the DewormingForm instance
            form_instance = form.save(commit=False)
            form_instance.vet_form = vet_deworming_form
            form_instance.save()

            messages.success(request, 'Details successfully saved')
            return redirect('vet-portal')

    else:
        form = DewormingForm()

    context = {
        'form': form,
        'name': 'Deworming Form'
    }

    return render(request, 'portals/forms.html', context)

@login_required    
def vaccination(request):
    if request.method == "POST":
        form = VaccinationForm(request.POST)
        if form.is_valid():
            # Create a new Vet_Forms instance with vet_username and is_vaccination_form
            vet_vaccination_form = Vet_Forms(vet_username=request.user, is_vaccination_form=True)
            vet_vaccination_form.save()

            # Associate the Vet_Forms instance with the VaccinationForm instance
            form_instance = form.save(commit=False)
            form_instance.vet_form = vet_vaccination_form
            form_instance.save()

            messages.success(request, 'Details successfully saved')
            return redirect('vet-portal')

    else:
        form = VaccinationForm()

    context = {
        'form': form,
        'name': 'Vaccination Form'
    }

    return render(request, 'portals/forms.html', context)

@login_required
def breeding_record(request):
    ...

@login_required
def artificial_insemination(request):
    if request.method == "POST":
        form = ArtificialInseminationForm(request.POST)
        if form.is_valid():
            # Create a new Vet_Forms instance with vet_username and is_artificial_insemination_form
            vet_ai_form = Vet_Forms(vet_username=request.user, is_artificial_insemination_form=True)
            vet_ai_form.save()

            # Associate the Vet_Forms instance with the ArtificialInseminationForm instance
            form_instance = form.save(commit=False)
            form_instance.vet_form = vet_ai_form
            form_instance.save()

            messages.success(request, 'Details successfully saved')
            return redirect('vet-portal')

    else:
        form = ArtificialInseminationForm()

    context = {
        'form': form,
        'name': 'Artificial Insemination Form'
    }

    return render(request, 'portals/forms.html', context)

@login_required
#@login_required  # Decorate your view with login_required to ensure the user is authenticated
def calf_registration(request):
    if request.method == "POST":
        form = CalfRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new Vet_Forms instance
            vet_calf_form = Vet_Forms(is_calf_registration_form=True)
            vet_calf_form.save()

            # Create a new Calf_Registration_Form instance
            form_instance = form.save(commit=False)

            # Extract the username from the user instance and assign it to farmer_username
            form_instance.farmer_username = request.user.username  # Change this line

            form_instance.vet_form = vet_calf_form
            form_instance.save()

            messages.success(request, 'Details successfully saved')
            return redirect('farmer-portal')    

    else:
        form = CalfRegistrationForm()

    context = {
        'form': form,
        'name': 'Calf Registration Form'
    }
    return render(request, 'portals/fforms.html', context)

@login_required
def calf_form_view(request):
    calf_forms = Calf_Registration_Form.objects.filter(farmer_username=request.user)
    context = {
        'form_name': 'Calf Registration Form',
        'forms': calf_forms
    }    
    return render(request, 'portals/fformview.html', context)


@login_required
def edit_calf_registration(request, pk):
	try:
		calf_sel = Calf_Registration_Form.objects.get(pk = pk)
	except Calf_Registration_Form.DoesNotExist:
		return redirect('index')
	calf_form = CalfRegistrationForm(request.POST or None, instance = calf_sel)
	if calf_form.is_valid():
		calf_form.save()
		return redirect('index')
	return render(request, 'portals/editfform.html', {'form':calf_form, 'form_name':'Calf Registration'})


@login_required
def livestock_inventory(request):
    if request.method == "POST":
        form = LivestockInventoryForm(request.POST)
        if form.is_valid():
            # Create a new Vet_Forms instance
            vet_inventory_form = Vet_Forms(is_livestock_inventory_form=True)
            vet_inventory_form.save()

            # Associate the Vet_Forms instance with the LivestockInventoryForm instance
            form_instance = form.save(commit=False)
            form_instance.vet_form = vet_inventory_form
            form_instance.save()

            messages.success(request, 'Details successfully saved')
            return redirect('farmer-portal')

    else:
        form = LivestockInventoryForm()

    context = {
        'form': form,
        'name': 'Livestock Inventory Form'
    }

    return render(request, 'portals/forms.html', context)

@login_required
def livestock_inventory_view(request):
    livestock_forms = Livestock_Inventory_Form.objects.filter(farmer_username=request.user)
    context = {
        'form_name': 'Livestock Inventory Form',
        'forms': livestock_forms
    }    
    return render(request, 'portals/livestockformview.html', context)


@login_required
def edit_livestock_inventory(request, pk):
	try:
		livestock_sel = Livestock_Inventory_Form.objects.get(pk = pk)
	except Livestock_Inventory_Form.DoesNotExist:
		return redirect('index')
	livestock_form = LivestockInventoryForm(request.POST or None, instance = livestock_sel)
	if livestock_form.is_valid():
		livestock_form.save()
		return redirect('index')
	return render(request, 'portals/editfform.html', {'form':livestock_form, 'form_name':'Livestock Inventory Form'})


@login_required
def pregnancy_diagnosis(request):
    if request.method == "POST":
        form = PregnancyDiagnosisForm(request.POST)
        if form.is_valid():
            # Create a new Vet_Forms instance with vet_username and is_pregnancy_diagnosis_form
            vet_preg_form = Vet_Forms(vet_username=request.user, is_pregnancy_diagnosis_form=True)
            vet_preg_form.save()

            # Associate the Vet_Forms instance with the PregnancyDiagnosisForm instance
            form_instance = form.save(commit=False)
            form_instance.vet_form = vet_preg_form
            form_instance.save()

            messages.success(request, 'Details successfully saved')
            return redirect('vet-portal')

    else:
        form = PregnancyDiagnosisForm()

    context = {
        'form': form,
        'name': 'Pregnancy Diagnosis Form'
    }

    return render(request, 'portals/forms.html', context)
 

@login_required
def consultation_form_view(request):
    consultation_forms = Farm_Consultation.objects.filter(vet_form__vet_username=request.user)
    context = {
        'form_name': 'Consultation Form',
        'forms': consultation_forms
    }    
    return render(request, 'portals/consultationformview.html', context)
 
    
@login_required
def edit_consultation_form(request, pk):
	try:
		consul_sel = Farm_Consultation.objects.get(pk = pk)
	except Farm_Consultation.DoesNotExist:
		return redirect('index')
	consultation_form = FarmConsultationForm(request.POST or None, instance = consul_sel)
	if consultation_form.is_valid():
		consultation_form.save()
		return redirect('index')
	return render(request, 'portals/editform.html', {'form':consultation_form, 'form_name':'Consultation'})

@login_required
def consultation(request):
    if request.method == "POST":
        form = FarmConsultationForm(request.POST)
        if form.is_valid():
            # Create a new Vet_Forms instance with is_farm_consultation set
            consultation_form = Vet_Forms(vet_username=request.user, is_farm_consultation=True)
            consultation_form.save()

            # Associate the Vet_Forms instance with the FarmConsultationForm instance
            form_instance = form.save(commit=False)
            form_instance.vet_form = consultation_form
            form_instance.save()

            messages.success(request, 'Details successfully saved')
            return redirect('vet-portal')

    else:
        form = FarmConsultationForm()

    context = {
        'form': form,
        'name': 'Farm Consultation Form'
    }

    return render(request, 'portals/forms.html', context)


@login_required
def vet_billing_form_view(request):
    bill_forms = Veterinary_Billing_Form.objects.filter(vet_form__vet_username=request.user)
    context = {
        'form_name': 'Vet Billing Form',
        'forms': bill_forms
    }    
    return render(request, 'portals/vetbillformview.html', context)
 
    
@login_required
def edit_vet_billing_form(request, pk):
	try:
		bill_sel = Veterinary_Billing_Form.objects.get(pk = pk)
	except Veterinary_Billing_Form.DoesNotExist:
		return redirect('index')
	billing_form = VeterinaryBillingForm(request.POST or None, instance = bill_sel)
	if billing_form.is_valid():
		billing_form.save()
		return redirect('index')
	return render(request, 'portals/editform.html', {'form':billing_form, 'form_name':'Vet Billing'})

@login_required
def vet_billing(request):
    if request.method == "POST":
        form = VeterinaryBillingForm(request.POST)
        if form.is_valid():
            # Create a new Vet_Forms instance with is_vet_billing_form set
            billing_form = Vet_Forms(vet_username=request.user, is_vet_billing_form=True)
            billing_form.save()

            # Associate the Vet_Forms instance with the VeterinaryBillingForm instance
            form_instance = form.save(commit=False)
            form_instance.vet_form = billing_form
            form_instance.save()

            messages.success(request, 'Details successfully saved')
            return redirect('vet-portal')

    else:
        form = VeterinaryBillingForm()

    context = {
        'form': form,
        'name': 'Vet Billing Form'
    }

    return render(request, 'portals/forms.html', context)


@login_required
def lab_form_view(request):
    lab_forms = Laboratory_Form.objects.filter(vet_form__vet_username=request.user)
    context = {
        'form_name': 'Laboratory Form',
        'forms': lab_forms
    }    
    return render(request, 'portals/labformview.html', context)
 
    
@login_required
def edit_lab_form(request, pk):
	try:
		lab_sel = Laboratory_Form.objects.get(pk = pk)
	except Laboratory_Form.DoesNotExist:
		return redirect('index')
	lab_form = LaboratoryForm(request.POST or None, instance = lab_sel)
	if lab_form.is_valid():
		lab_form.save()
		return redirect('index')
	return render(request, 'portals/editform.html', {'form':lab_form, 'form_name':'Laboratory'})

@login_required
def lab(request):
    if request.method == "POST":
        form = LaboratoryForm(request.POST)
        if form.is_valid():
            # Create a new Vet_Forms instance with is_lab_form set
            labo_form = Vet_Forms(is_lab_form=True)
            labo_form.save()

            # Associate the Vet_Forms instance with the LaboratoryForm instance
            form_instance = form.save(commit=False)
            form_instance.vet_form = labo_form
            form_instance.save()

            messages.success(request, 'Details successfully saved')
            return redirect('vet-portal')

    else:
        form = LaboratoryForm()

    context = {
        'form': form,
        'name': 'Laboratory Form'
    }

    return render(request, 'portals/forms.html', context)



@login_required
def referral_form_view(request):
    referral_forms = Referral_Form.objects.filter(vet_form__vet_username=request.user)
    context = {
        'form_name': 'Referral Form',
        'forms': referral_forms
    }    
    return render(request, 'portals/referralformview.html', context)


@login_required 
def referral_form(request):
    if request.method == "POST":
        form = ReferalForm(request.POST)
        if form.is_valid():
            referral_form= Vet_Forms(vet_username=request.user, is_referral_form=True)
            referral_form.save() 
            form.save()
            messages.success(request, 'Details  Successfully Saved')
            return redirect('vet-portal')    

    else:
        form = ReferalForm()

    context = {
        'form':form,
        'name':'Referral form'
         }
    return render(request, 'portals/forms.html', context)




class referral_Form_Pdf(View):

    def get(self, request):
        try:
            referral_forms = Referral_Form.objects.filter(farmer_username=request.user)
        except:
            messages.warning(self.request, f'referral form for {request.user} not available')
            return redirect('farmer-portal')    
        if referral_forms:
            params = {
                'today':timezone.now,
                'forms': referral_forms,
                'request': request          
            }
            return Render.render('portals/referral_pdf_form.html', params)
        else:
            messages.warning(self.request, f'No referral form available for {self.request.user}')
            return redirect('index')    


class Referral_Form_Pdf_Vet(View):

    def get(self, request):
        try:
            referral_forms = Referral_Form.objects.filter(vet_form__vet_username=self.request.user)
        except:
            messages.warning(self.request, f'referral form for {request.user} not available')
            return redirect('vet-portal')    
        if referral_forms:
            params = {
                'today':timezone.now,
                'forms': referral_forms,
                'request': request
            }
            return Render.render('portals/referral_pdf_form.html', params)
        else:
            messages.warning(self.request, f'No referral form available for {self.request.user}')
            return redirect('index') 


@login_required
def edit_referral_form(request, pk):
	try:
		referral_sel = Referral_Form.objects.get(pk = pk)
	except Referral_Form.DoesNotExist:
		return redirect('index')
	referral_form = ReferalForm(request.POST or None, instance = referral_sel)
	if referral_form.is_valid():
		referral_form.save()
		return redirect('index')
	return render(request, 'portals/editform.html', {'form':referral_form, 'form_name':'referral'})

def sick_form_pdf(request):
    farmer = Farmer.objects.get(user=request.user)
    sick_forms = Sick_Approach_Form.objects.filter(farmer=farmer)
    if sick_forms:
        pdf = FPDF('P', 'mm', 'A4')
        for form in sick_forms:
            print(form)
            pdf.add_page()
            pdf.set_font('courier', 'B', 16)
            pdf.cell(40, 10, 'Clinical Approach Form',0,1)
            #pdf.cell(40, 10, f'{form.vet_form.report_created_on}', 0, 1)
            pdf.cell(40, 10, '',0,1)
            pdf.set_font('courier', '', 12)
            pdf.cell(200, 8, f"{'Field'.ljust(30)} {'Value'.rjust(30)}", 0, 1)
            pdf.line(10, 30, 200, 30)
            pdf.line(10, 38, 200, 38)

            pdf.cell(200, 8, f"{'Species affected'.ljust(30)} {form.species_affected.rjust(30)}", 0, 1)
            pdf.cell(200, 8, f"{'Number of Species affected'.ljust(30)} {str(form.num_of_species_affected).rjust(30)}", 0, 1)
            pdf.cell(200, 8, f"{'Identification number'.ljust(30)} {form.id_animal.rjust(30)}", 0, 1)
            pdf.cell(200, 8, f"{'nature of the disease'.ljust(30)} {form.disease_nature.rjust(30)}", 0, 1)
            pdf.cell(200, 8, f"{'Clinical Signs'.ljust(30)} {form.clinical_signs.rjust(30)}", 0, 1)
            pdf.cell(200, 8, f"{'Disease Diagnosis'.ljust(30)} {form.disease_diagnosis.rjust(30)}", 0, 1)
            pdf.cell(200, 8, f"{'Differential Diagnosis'.ljust(30)} {form.differential_diagnosis.rjust(30)}", 0, 1)
            pdf.cell(200, 8, f"{'Final Diagnosis'.ljust(30)} {form.final_diagnosis.rjust(30)}", 0, 1)
            pdf.cell(200, 8, f"{'Duration of the sickness '.ljust(30)} {form.sickness_duration.rjust(30)}", 0, 1)
            # more cells here ...


        pdf.output('clinical_approach_report.pdf', 'F')
        return FileResponse(open('clinical_approach_report.pdf', 'rb'), as_attachment=False, content_type='application/pdf')

    else:
        messages.warning(request, f'No referral form available for {request.user}')
        return redirect('farmer-portal') 
class Sick_Form_Pdf(View):

    def get(self, request):
        try:
            sick_forms = Sick_Approach_Form.objects.filter(farmer_username=request.user)
        except:
            messages.warning(self.request, f'Sick approach form for {request.user} not available')
            return redirect('farmer-portal')    
        if sick_forms:
            params = {
                'today':timezone.now,
                'forms': sick_forms,
                'request': request          
            }
            return Render.render('portals/sick_form_pdf.html', params)
        else:
            messages.warning(self.request, f'No Sick form available for {self.request.user}')
            return redirect('index')    


class Sick_Form_Pdf_Vet(View):

    def get(self, request):
        try:
            sick_forms = Sick_Approach_Form.objects.filter(vet_form__vet_username=self.request.user)
        except:
            messages.warning(self.request, f'Sick approach form for {request.user} not available')
            return redirect('vet-portal')    
        if sick_forms:
            params = {
                'today':timezone.now,
                'forms': sick_forms,
                'request': request
            }
            return Render.render('portals/sick_form_pdf.html', params)
        else:
            messages.warning(self.request, f'No Sick form available for {self.request.user}')
            return redirect('index') 



def dead_form_pdf(request):
    dead_forms = Death_Approach_Form.objects.filter(farmer_username=request.user)
    if dead_forms:
        pdf = FPDF('P', 'mm', 'A4')
        for form in dead_forms:
            pdf.add_page()
            pdf.set_font('courier', 'B', 16)
            pdf.cell(40, 10, 'Post Mortem Approach Form',0,1)
            pdf.cell(40, 10, '',0,1)
            pdf.set_font('courier', '', 12)
            pdf.cell(200, 8, f"{'Field'.ljust(30)} {'Value'.rjust(30)}", 0, 1)
            pdf.line(10, 30, 200, 30)
            pdf.line(10, 38, 200, 38)

            pdf.cell(200, 8, f"{'Name or identification number'.ljust(30)} {form.name_of_the_animal.rjust(30)}", 0, 1)
            pdf.cell(200, 8, f"{'Sex of the animal'.ljust(30)} {str(form.sex_of_the_animal).rjust(30)}", 0, 1)
            pdf.cell(200, 8, f"{'Number of animals dead'.ljust(30)} {str(form.num_of_species_dead).rjust(30)}", 0, 1)
            pdf.cell(200, 8, f"{'When was the case reported'.ljust(30)} {form.case_history.rjust(30)}", 0, 1)
            # more cells here ...
            


        pdf.output('postmortem_approach_report.pdf', 'F')
        return FileResponse(open('postmortem_approach_report.pdf', 'rb'), as_attachment=False, content_type='application/pdf')

    else:
        messages.warning(request, f'Post Mortem form for {request.user} is  not available')
        return redirect('farmer-portal')




class Dead_Form_Pdf(View):

    def get(self, request):
        try:
            dead_forms = Death_Approach_Form.objects.filter(farmer_username=request.user)
        except: 
            messages.warning(self.request, f'Sick approach form for {request.user} not available')
            return redirect('farmer-portal')
        if dead_forms:
            params = {
                'today':timezone.now,
                'forms': dead_forms,
                'request': request
            }
            return Render.render('portals/dead_form_pdf.html',params)
        else:
            messages.warning(self.request,f'No dead form available for {self.request.user}')
            return redirect('index')


class Dead_Form_Pdf_Vet(View):

    def get(self, request):
        try:
            dead_forms = DeathApproachForm.objects.filter(vet_form__vet_username=self.request.user)
        except:
            messages.warning(self.request, f'Death approach form for {request.user} not available')
            return redirect('vet-portal')    
        if dead_forms:
            params = {
                'today':timezone.now,
                'forms': dead_forms,
                'request': request
            }
            return Render.render('portals/dead_form_pdf.html', params)
        else:
            messages.warning(self.request, f'No Sick form available for {self.request.user}')
            return redirect('index') 


class Surgical_Form_Pdf(View):

    def get(self, request):
        try:
            surgical_forms = Surgical_Approach_Form.objects.filter(farmer_username=request.user)
        except:
            messages.warning(self.request, f'Sick approach form for {request.user} not available')
            return redirect('farmer-portal')
        if surgical_forms:
            params = {
                'today':timezone.now,
                'forms': surgical_forms,
                'request': request
            }
            return Render.render('portals/surgical_form_pdf.html',params)
        else:
            messages.warning(self.request,f'No surgical form available for {self.request.user}')
            return redirect('index')


class Deworming_Form_Pdf(View):

    def get(self, request):
        try:
            deworming_forms = Deworming_Form.objects.filter(farmer_username=request.user)
        except:
            messages.warning(self.request, f'Sick approach form for {request.user} not available')
            return redirect('farmer-portal')
        if deworming_forms:
            params = {
                'today':timezone.now,
                'forms': deworming_forms,
                'request': request
            }
            return Render.render('portals/deworming_form_pdf.html', params)
        else:
            messages.warning(self.request, f'No deworming form available for {self.request.user}')
            return redirect('index')    


class Vaccination_Form_Pdf(View):

    def get(self, request):
        try:
            vaccination_forms = Vaccination_Form.objects.filter(farmer_username=request.user)
        except:
            messages.warning(self.request, f'Sick approach form for {request.user} not available')
            return redirect('farmer-portal')
        if vaccination_forms:
            params = {
                'today':timezone.now,
                'forms': vaccination_forms,
                'request': request
            }
            return Render.render('portals/vaccination_pdf_form.html', params)
        else:
            messages.warning(self.request, f'No vaccination form available for {self.request.user}')
            return redirect('index') 


class Artificial_Insemination_Form_Pdf(View):

    def get(self, request):
        try:
            Artificial_forms = Artificial_Insemination_Form.objects.filter(farmer_username=request.user)
        except:
            messages.warning(self.request, f'Sick approach form for {request.user} not available')
            return redirect('farmer-portal')
        if Artificial_forms:
            params = {
                'today':timezone.now,
                'forms': Artificial_forms,
                'request': request
            }
            return Render.render('portals/artificial_form_pdf.html', params)
        else:
            messages.warning(self.request, f'No artificial form available for {self.request.user}')
            return redirect('index') 



class Farm_Consultation_Form_Pdf(View):

    def get(self, request):
        try:
            consultation_forms = Farm_Consultation.objects.filter(farmer_username=request.user)
        except:
            messages.warning(self.request, f'Sick approach form for {request.user} not available')
            return redirect('farmer-portal')
        if consultation_forms:
            params = {
                'today':timezone.now,
                'forms': consultation_forms,
                'request': request
            }
            return Render.render('portals/consultation_form.html', params)
        else:
            messages.warning(self.request, f'No consultation form available for {self.request.user}')
            return redirect('index') 


class Pregnancy_Diagnosis_Form_Pdf(View):

    def get(self, request):
        diagnosis_forms = Pregnancy_Diagnosis_Form.objects.filter(farmer_username=request.user)
        if diagnosis_forms:
            params = {
                'today':timezone.now,
                'forms': diagnosis_forms,
                'request': request
            }
            return Render.render('portals/diagnosis_form.html', params)
        else:
            messages.warning(self.request, f'No pregnancy form available for {self.request.user}')
            return redirect('index') 

class Calf_Registration_Form_Pdf(View):

    def get(self, request):
        calf_reg_forms = Calf_Registration_Form.objects.filter(farmer_username=request.user)
        if calf_reg_forms:
            params = {
                'today':timezone.now,
                'forms': calf_reg_forms,
                'request': request
            }
            return Render.render('portals/calf_reg_form.html', params)
        else:
            messages.warning(self.request, f'No Calf registration form available for {self.request.user}')
            return redirect('index') 

class Livestock_Form_Pdf(View):

    def get(self, request):
        livestock_forms = Livestock_Inventory_Form.objects.filter(farmer_username=request.user)
        if livestock_forms:
            params = {
                'today':timezone.now,
                'forms': livestock_forms,
                'request': request
            }
            return Render.render('portals/livestock_form.html', params)
        else:
            messages.warning(self.request, f'No Livestock form available for {self.request.user}')
            return redirect('index') 



def display_images(request):
    inventory = Livestock_Inventory_Form.objects.get(farmer_username=request.user)
    context = {
        'img_obj': inventory
    }
    return render(request, 'portals/gallery.html', context)


    #records
def artificial_report(request):
    
    return render(request,'portals/reports/artificialinsemination.html')

def artificial_report_data(request):
    artificial_approach_forms = Artificial_Insemination_Form.objects.all()
    data = []
    for form in artificial_approach_forms:
        data.append({
            'farmer_username': form.farmer_username,
            'Name_of_the_cow': form.Name_of_the_cow,
            'sex_of_the_calf_born': form.sex_of_the_calf_born,
            'date_of_birth': form.date_of_birth,
            'nature_of_birth': form.nature_of_birth,
            'number_of_repeat': form.number_of_repeat,
            'abortion_rate': form.abortion_rate,
            'reason_for_the_cause_of_abortion': form.reason_for_the_cause_of_abortion,
            'time_of_heat_sign': form.time_of_heat_sign,
            'date_of_insemination': form.date_of_insemination,
            'time_of_insemination': form.time_of_insemination,
            'nature_of_the_breeding': form.nature_of_the_breeding,
            'sire_name': form.sire_name,
            'sire_origin': form.sire_origin,
            'bull_code': form.bull_code,
            'breed_used': form.breed_used,
            'source_of_semen': form.source_of_semen,
            'date_of_repeat_checked': form.date_of_repeat_checked,
            'date_of_pregnancy_diagnosis': form.date_of_pregnancy_diagnosis,
            'expected_date_of_calving': form.expected_date_of_calving,
            'comment': form.comment,
        })

    return JsonResponse({'data': data}, safe=False)

def deworming_report(request):
    
    return render(request,'portals/reports/deworming.html')


def deworming_report_data(request):
    deworming_forms = Deworming_Form.objects.all() 

    data = []
    for form in deworming_forms:
        data.append(
        {
            'farmer_username': form.farmer_username,
            'species_targeted': form.species_targeted,
            'number_of_adults': form.number_of_adults,
            'number_of_young_ones': form.number_of_young_ones,
            'body_condition_of_the_animal': form.body_condition_of_the_animal,
            'date_of_deworming': form.date_of_deworming,
            'drug_choices': form.drug_choices,
            'target_parasites': form.target_parasites,
            'withdrawal_period': form.withdrawal_period,
            'side_effects': form.side_effects,
            'next_date_deworming': form.next_date_deworming,
            'comment': form.comment,
        })
      
    

    return JsonResponse({'data': data}, safe=False)



def sick_report_data(request):
    sick_reports = Sick_Approach_Form.objects.all() 

    data = []
    for report in sick_reports:
        data.append(
        {
            'farmer_username': report.farmer.farmer_username,
            'species_affected': report.species_affected,
            'num_of_species_affected': report.num_of_species_affected,
            'id_animal': report.id_animal,
            'disease_nature': report.disease_nature,
            'clinical_signs': report.clinical_signs,
            'disease_diagnosis': report.disease_diagnosis,
            'differential_diagnosis': report.differential_diagnosis,
            'final_diagnosis': report.final_diagnosis,
            'sickness_duration': report.sickness_duration,
            'sickness_history': report.sickness_history,
            'drug_of_choice': report.drug_of_choice,
            'treatment_duration': report.treatment_duration,
            'start_dose_date': report.start_dose_date,
            'prognosis': report.prognosis,
            'harmony_with_clinic_signs_and_lab': report.harmony_with_clinic_signs_and_lab,
            'cause_of_death_if_in_no_harmony': report.cause_of_death_if_in_no_harmony,
            'disease_one_of_the_zoonotic': report.disease_one_of_the_zoonotic,
            'advice_given_if_zoonotic': report.advice_given_if_zoonotic,
            'relapse': report.relapse,
            'cause_if_relapse': report.cause_if_relapse,
            'comment': report.comment,
        })
       
    return JsonResponse({'data': data}, safe=False)
def sick_report(request):
    
    return render(request, 'portals/reports/sickness.html')

def death_report_data(request):
    death_reports = Death_Approach_Form.objects.all()

    data = []
    for report in death_reports:
        data.append(
        {
            'vet_form_id': report.vet_form_id,
            'farmer_username': report.farmer_username,
            'name_of_the_animal': report.name_of_the_animal,
            'sex_of_the_animal': report.sex_of_the_animal,
            'num_of_species_dead': report.num_of_species_dead,
            'case_history': report.case_history,
            'mortality_rate': report.mortality_rate,
            'death_date': report.death_date,
            'death_time': report.death_time,
            'signs_of_cadever_on_the_ground': report.signs_of_cadever_on_the_ground,
            'carcass_opened_for_the_pm': report.carcass_opened_for_the_pm,
            'if_yes_pathological_signs': report.if_yes_pathological_signs,
            'if_no_reason': report.if_no_reason,
            'sample_sent_lab': report.sample_sent_lab,
            'if_yes_lab_report': report.if_yes_lab_report,
            'death_cause_notifiable': report.death_cause_notifiable,
            'if_yes_message_to_relevant_body': report.if_yes_message_to_relevant_body,
            'intervention_regards_to_death': report.intervention_regards_to_death,
            'comment': report.comment,
        })
       

    return JsonResponse({'data': data}, safe=False)

def death_report(request):
   
    return render(request, 'portals/reports/death.html')

def surgical_report(request):
   
    return render(request, 'portals/reports/surgery.html')

def surgical_report_data(request):
    surgical_reports = Surgical_Approach_Form.objects.all()

    data = []
    for report in surgical_reports:
        data.append(
        {
            'vet_form_id': report.vet_form_id,
            'farmer_username': report.farmer_username,
            'species_operated_on': report.species_operated_on,
            'if_other_specify_species': report.if_other_specify,
            'sex_of_the_animal': report.sex_of_the_animal,
            'name_of_the_animal': report.name_of_the_animal,
            'operation_nature': report.operation_nature,
            'if_other_specify_operation': report.if_other_specify,
            'operation_date': report.operation_date,
            'post_operation_management': report.post_operation_management,
            'prognosis': report.prognosis,
            'comment': report.comment,
        })
       

    return JsonResponse({'data': data}, safe=False)
def vaccination_report_data(request):
    vaccination_reports = Vaccination_Form.objects.all()

    data = []
    for report in vaccination_reports:
         data.append(
        {
            'vet_form_id': report.vet_form_id,
            'farmer_username': report.farmer_username,
            'species_targeted': report.species_targeted,
            'if_other_specify_species': report.if_other_specify,
            'number_of_animals_vaccinated': report.number_of_animals_vaccinated,
            'age_of_animal': report.age_of_animal,
            'sex_of_the_animal': report.sex_of_the_animal,
            'animal_breed': report.animal_breed,
            'animal_colour': report.animal_colour,
            'other_description': report.other_description,
            'targetted_disease': report.targetted_disease,
            'vaccines_used': report.vaccines_used,
            'date_of_vaccination': report.date_of_vaccination,
            'next_date_of_vaccination': report.next_date_of_vaccination,
            'name_of_the_crush': report.name_of_the_crush,
            'nature_of_the_vaccination_program': report.nature_of_the_vacination_program,
            'comment': report.comment,
        })
       

    return JsonResponse({'data': data}, safe=False)

    
def vaccination_report(request):
   
    return render(request, 'portals/reports/vaccination.html')


def pregnancy_diagnosis_report_data(request):
    pregnancy_diagnosis_reports = Pregnancy_Diagnosis_Form.objects.all()

    data = []
    for report in pregnancy_diagnosis_reports:
        data.append(
            {
                'vet_form_id': report.vet_form_id,
                'farmer_username': report.farmer_username,
                'cow_name': report.cow_name,
                'cow_category': report.cow_category,
                'date_of_insemination': report.date_of_insemination,
                'date_of_pregnancy_diagnosis': report.date_of_pregnancy_diagnosis,
                'result_of_diagnosis': report.result_of_diagnosis,
                'if_positive': report.if_positive,
                'if_result_is_negative_give_observation': report.if_result_is_negative_give_observation,
                'next_date_of_pregnancy_diagnosis': report.next_date_of_pregnancy_diagnosis,
                'expected_date_of_delivery': report.expected_date_of_delivery,
                'comment': report.comment,
            })
      
    

    return JsonResponse({'data': data}, safe=False)

def pregnancy_diagnosis_report(request):
    
    return render(request, 'portals/reports/pregnancydiagnosis.html')

def farm_consultation_report_data(request):
    farm_consultation_reports = Farm_Consultation.objects.all()

    data = []
    for report in farm_consultation_reports:
         data.append(
        {
            'vet_form_id': report.vet_form_id,
            'farmer_username': report.farmer_username,
            'dairy_cows': report.dairy_cows,
            'beef_production': report.beef_production,
            'poultry': report.poultry,
            'sheep': report.sheep,
            'goat': report.goat,
            'canine': report.canine,
            'other': report.other,
            'give_recommendation': report.give_recommendation,
            'grazing': report.grazing,
            'disease': report.disease,
            'farm': report.farm,
            'culling_selection': report.culling_selection,
            'farm_manager': report.farm_manager,
            'if_no': report.if_no,
            'name_incharge': report.name_incharge,
            'reg_number': report.reg_number,
            'comment': report.comment,
        })
       
    return JsonResponse({'data': data}, safe=False)

def farm_consultation_report(request):
   
    return render(request, 'portals/reports/farmconsultation.html')

def veterinary_billing_report_data(request):
    veterinary_billing_forms = Veterinary_Billing_Form.objects.all()

    data = []
    for form in veterinary_billing_forms:
         data.append(
        {
            'vet_form_id': form.vet_form_id,
            'farmer_username': form.farmer_username,
            'Mobile_number': form.Mobile_number,
            'farmer_location': form.farmer_location,
            'nature_of_problem': form.nature_of_problem,
            'bill_paid': form.bill_paid,
            'total_bill': form.total_bill,
            'balance_due': form.balance_due,
            'agreed_date': form.agreed_date,
            'suggest_payment': form.suggest_payment,
            'vet_name': form.vet_name,
            'registration_number': form.registration_number,
            'Mobile_number_vet': form.Mobile_number_vet,
            'comment': form.comment,
        })
        
    return JsonResponse({'data': data}, safe=False)

def veterinary_billing_report(request):
    
    return render(request, 'portals/reports/veterinarybilling.html')

def laboratory_report_data(request):
    laboratory_forms = Laboratory_Form.objects.all()

    data = []
    for form in laboratory_forms:
        data.append({
            'vet_form_id': form.vet_form_id,
            'farmer_username': form.farmer_username,
            'Mobile_number': form.Mobile_number,
            'category_ssp': form.category_ssp,
            'sample': form.sample,
            'name_animal': form.name_animal,
            'date_of_submission': form.date_of_submission,
            'idenfication': form.idenfication,
            'storage': form.storage,
            'transportation': form.transportation,
            'expected_duration': form.expected_duration,
            'sample_collected_sick_animal': form.sample_collected_sick_animal,
            'sample_collected_dead': form.sample_collected_dead,
            'if_yes_sick': form.if_yes_sick,
            'findings': form.findings,
            'vet_name': form.vet_name,
            'registration_number_vet': form.registration_number_vet,
            'Mobile_number_vet': form.Mobile_number_vet,
            'laboratory_officer': form.laboratory_officer,
            'registration_number_lab_officer': form.registration_number_lab_officer,
            'Mobile_number_lab_officer': form.Mobile_number_lab_officer,
            'comment': form.comment,
        })

    return JsonResponse({'data': data}, safe=False)

def laboratory_report(request):
   
    return render(request, 'portals/reports/laboratory.html')
def referral_report_data(request):
    referral_forms = Referral_Form.objects.all()

    data = []
    for form in referral_forms:
        data.append({
            'vet_form_id': form.vet_form_id,
            'farmer_username': form.farmer_username,
            'Mobile_number': form.Mobile_number,
            'case_referal': form.case_referal,
            'previous_treated': form.previous_treated,
            'state_prognosis': form.state_prognosis,
            'referal_date': form.referal_date,
            'suggest_vet': form.suggest_vet,
            'if_yes_leave_phone_number': form.if_yes_leave_phone_number,
            'registration_number_vet': form.registration_number_vet,
            'comment': form.comment,
        })

    return JsonResponse({'data': data}, safe=False)

def referral_report(request):
  
    return render(request, 'portals/reports/referral.html')

def livestock_inventory_report_data(request):
    livestock_forms = Livestock_Inventory_Form.objects.all()

    data = []
    for form in livestock_forms:
        data.append({
            'vet_form_id': form.vet_form_id,
            'farmer_username': form.farmer_username,
            'species_targeted': form.species_targeted,
            'name_of_the_animal': form.name_of_the_animal,
            'number_of_the_male_animals': form.number_of_the_male_animals,
            'number_of_the_female_animals': form.number_of_the_female_animals,
            'number_of_live_animals': form.number_of_live_animals,
            'number_of_dead_animals': form.number_of_dead_animals,
            'specify_the_cause_of_the_dead': form.specify_the_cause_of_the_dead,
            'is_your_animals_insured': form.is_your_animals_insured,
            'if_yes_give_insuring_company': form.if_yes_give_insuring_company,
            'date_of_culling': form.date_of_culling,
            'give_reason_for_culling': form.give_reason_for_culling,
            'comment': form.comment,
        })

    return JsonResponse({'data': data}, safe=False)

def livestock_inventory_report(request):
   
    return render(request, 'portals/reports/inventory.html')


# Define views
def calf(request):
    return render(request, 'portals/farmer/calf.html', {})

class CalfCreate(generics.CreateAPIView):
    queryset = Calf.objects.all()
    serializer_class = CalfSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CalfList(generics.ListAPIView):
    serializer_class = CalfSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        #print(user)
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


# dead animal
@login_required
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
        #print(user)
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
@login_required
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
        #print(user)
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
@login_required
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
        #print(user)
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
@login_required
def new_animal(request):
    return render(request, 'portals/farmer/new.html', {})
class NewAnimalCreate(generics.CreateAPIView):
    queryset = NewAnimal.objects.all()
    serializer_class = NewAnimalSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NewAnimalList(generics.ListAPIView):
    serializer_class = NewAnimalSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        #print(user)
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
@login_required
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
        #print(user)
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
    serializer_class = DairyHygieneSerializer
    permission_classes = [Is_Farmer]

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()


def salaries(request):
    return render(request, 'portals/farmer/salaries.html', {})
class SalariesCreate(generics.CreateAPIView):
    queryset = Salaries.objects.all()
    serializer_class = SalariesSerializer
    permission_classes = [Is_Farmer]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SalariesList(generics.ListAPIView):
    serializer_class = SalariesSerializer
    permission_classes = [Is_Farmer]
    pagination_class = CustomPagination  # If you have a custom pagination class

    def get_queryset(self):
        user = self.request.user
        return LivestockInsurance.objects.filter(user=user).order_by('-id')

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


def employees(request):
    return render(request, 'portals/farmer/employment.html', {})

class EmployeesCreate(generics.CreateAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer
    permission_classes = [Is_Farmer]  # Replace with your custom permission class if needed

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EmployeesList(generics.ListAPIView):
    serializer_class = EmployeesSerializer
    permission_classes = [Is_Farmer]  
    pagination_class = CustomPagination  

    def get_queryset(self):
        user = self.request.user
        return Employees.objects.filter(user=user).order_by('-id')

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

def lactation(request):
    return render(request, 'portals/farmer/lactation.html', {})

class LactatingCowCreate(generics.CreateAPIView):
    queryset = LactatingCow.objects.all()
    serializer_class = LactatingCowSerializer
    permission_classes = [Is_Farmer]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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

def milk_record(request):
    return render(request, 'portals/farmer/milk_records.html', {})

class MilkRecordCreate(generics.CreateAPIView):
    queryset = MilkRecord.objects.all()
    serializer_class = MilkRecordSerializer
    permission_classes = [Is_Farmer]

    def perform_create(self, serializer):
        # Set the employee to the first employee in the database and user to the request user
        employee = Employees.objects.first()
        serializer.save(employee_name=employee, user=self.request.user)
        
        # Get the date of the milk record
        milk_record_date = serializer.instance.date
        
        # Calculate the start of the week (Monday)
        week_start_date = milk_record_date - timedelta(days=milk_record_date.weekday())
        
        # Calculate the start of the month
        month_start_date = milk_record_date.replace(day=1)
        
        # Update or create weekly record
        weekly_record, created = WeeklyMilkRecord.objects.get_or_create(
            cow_name=serializer.instance.cow_name,
            week_start_date=week_start_date,
            defaults={'total_quantity': 0.0}
        )
        # Calculate total quantity for the week and update the record
        total_weekly_quantity = MilkRecord.objects.filter(
            cow_name=serializer.instance.cow_name,
            date__range=[week_start_date, week_start_date + timedelta(days=6)]
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0.0
        weekly_record.total_quantity = total_weekly_quantity
        weekly_record.save()
        
        # Update or create monthly record
        monthly_record, created = MonthlyMilkRecord.objects.get_or_create(
            cow_name=serializer.instance.cow_name,
            month=month_start_date,
            defaults={'total_quantity': 0.0}
        )
        # Calculate total quantity for the month and update the record
        total_monthly_quantity = MilkRecord.objects.filter(
            cow_name=serializer.instance.cow_name,
            date__year=milk_record_date.year,
            date__month=milk_record_date.month
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0.0
        monthly_record.total_quantity = total_monthly_quantity
        monthly_record.save()

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