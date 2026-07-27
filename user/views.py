from django.shortcuts import render, redirect

from . import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# from django.views.generic import CreateView
#from django.views.generic import View

from django.contrib.auth import get_user_model, logout

from django.contrib.auth import login, authenticate
from .models import User, Vet_Officer, Farmer, Official,DairyCooperative,Agrovet
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.permissions import BasePermission   



User = get_user_model()

def vet0fficer_signup_view(request):
	if request.method == 'POST':
		form = forms.VetOfficerSignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_vet_officer = True
			user.first_name = form.cleaned_data.get('first_name')
			user.last_name = form.cleaned_data.get('last_name')
			user.email = form.cleaned_data.get('email')
			user.phone_number = form.cleaned_data.get('phone_number')
			user.save()
			vet_officer = Vet_Officer.objects.create(user=user)
			vet_officer.kvb_number = form.cleaned_data.get('kvb_number')
			vet_officer.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}. You can now login')
			return redirect('vet-login')

	else:
		form = forms.VetOfficerSignUpForm()

	context = {
		'form':form
	}

	return render(request, 'user/vetregister.html', context)
	
def Official_signup_view(request):
	if request.method == 'POST':
		form = forms.OfficialSignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_official = True
			user.first_name = form.cleaned_data.get('first_name')
			user.last_name = form.cleaned_data.get('last_name')
			user.email = form.cleaned_data.get('email')
			user.phone_number = form.cleaned_data.get('phone_number')
			user.save()
			official = Official.objects.create(user=user)
			official.employment_number = form.cleaned_data.get('employment_number')
			official.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}. You can now login')
			return redirect('official-login')

	else:
		form = forms.OfficialSignUpForm()

	context = {
		'form':form
	}

	return render(request, 'user/official.html', context)


def Agrovet_signup_view(request):
	if request.method == 'POST':
		form = forms.AgrovetSignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_agrovet = True
			user.first_name = form.cleaned_data.get('first_name')
			user.last_name = form.cleaned_data.get('last_name')
			user.email = form.cleaned_data.get('email')
			user.phone_number = form.cleaned_data.get('phone_number')
			user.save()
			agrovet = Agrovet.objects.create(user=user)
			agrovet.agrovet_name = form.cleaned_data.get('agrovet_name')
			agrovet.vmd_number = form.cleaned_data.get('vmd_number')
			agrovet.qualification = form.cleaned_data.get('qualification')
			agrovet.county = form.cleaned_data.get('county')
			agrovet.subcounty = form.cleaned_data.get('subcounty')
			agrovet.town = form.cleaned_data.get('town')
			agrovet.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}. You can now login')
			return redirect('agrovet-login')

	else:
		form = forms.AgrovetSignUpForm()

	context = {
		'form':form
	}

	return render(request, 'user/agroregister.html', context)


def farmer_signup_view(request):
	if request.method == 'POST':
		form = forms.FarmerSignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_farmer = True
			user.first_name = form.cleaned_data.get('first_name')
			user.last_name = form.cleaned_data.get('last_name')
			user.email = form.cleaned_data.get('email')
			user.phone_number = form.cleaned_data.get('phone_number')
			user.save()
			farmer = Farmer.objects.create(user=user)
			farmer.farm_name = form.cleaned_data.get('farm_name')
			farmer.location = form.cleaned_data.get('location')
			farmer.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}. You can now login')
			return redirect('farmer-login')

	else:
		form = forms.FarmerSignUpForm()

	context = {
		'form':form
	}

	return render(request, 'user/farmerregister.html', context)

def cooperative_signup_view(request):
	if request.method == 'POST':
		form = forms.CooperativeSignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_cooperative = True
			user.first_name = form.cleaned_data.get('first_name')
			user.last_name = form.cleaned_data.get('last_name')
			user.email = form.cleaned_data.get('email')
			user.phone_number = form.cleaned_data.get('phone_number')
			user.save()
			cooperative = DairyCooperative.objects.create(user=user)
			cooperative.cooperative_name = form.cleaned_data.get('cooperative_name')
			cooperative.sub_county = form.cleaned_data.get('sub_county')
			cooperative.location = form.cleaned_data.get('location')
			cooperative.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}. You can now login')
			return redirect('cooperative-login')

	else:
		form = forms.CooperativeSignUpForm()

	context = {
		'form':form
	}

	return render(request, 'user/cooperativereg.html', context)



def agrovet_login(request):
	form = AuthenticationForm()
	if request.method == 'POST':  
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		
		if user is not None:
			# Check if any user is already logged in, log them out first
			if request.user.is_authenticated:
				logout(request)
			
			if user.is_authenticated and user.is_agrovet:
				login(request, user)
				return redirect('agrovet-portal')
			elif user.is_authenticated and user.is_farmer:
				messages.warning(request, 'Kindly login as a farmer')
				return redirect('farmer-login')
		else:
			messages.error(request, 'Invalid Credentials')

	return render(request, 'user/agrologin.html', {'form': form})
		

def vet_login(request):
	form = AuthenticationForm()
	if request.method == 'POST':  
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		
		if user is not None:
			# Check if any user is already logged in, log them out first
			if request.user.is_authenticated:
				logout(request)
			
			if user.is_authenticated and user.is_vet_officer:
				login(request, user)
				return redirect('vet-portal')
			elif user.is_authenticated and user.is_farmer:
				messages.warning(request, 'Kindly login as a farmer')
				return redirect('farmer-login')
		else:
			messages.error(request, 'Invalid Credentials')

	return render(request, 'user/vetlogin.html', {'form': form})

def official_login(request):
	form = AuthenticationForm()
	if request.method == 'POST':  
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		
		if user is not None:
			# Check if any user is already logged in, log them out first
			if request.user.is_authenticated:
				logout(request)
			
			if user.is_authenticated and user.is_official:
				login(request, user)
				return redirect('official-portal')
			elif user.is_authenticated and user.is_farmer or user.is_vet_officer:
				messages.warning(request, 'Kindly login as oficial')
				return redirect('official-login')

			elif user.is_authenticated and user.is_vet_officer:
				messages.warning(request, 'Kindly login as a veterinary  officer')
				return redirect('vet-login')
		else:
			messages.error(request, 'Invalid Credentials')

	return render(request, 'user/officiallogin.html', {'form': form})

def cooperative_login(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if user.is_cooperative:
                login(request, user)
                return redirect('cooperative-portal')

            elif user.is_farmer:
                messages.warning(
                    request,
                    'Kindly login as a Farmer.'
                )
                return redirect('farmer-login')

            elif user.is_vet_officer:
                messages.warning(
                    request,
                    'Kindly login as a Veterinary Officer.'
                )
                return redirect('vet-login')

            elif user.is_official:
                messages.warning(
                    request,
                    'Kindly login as a Government Official.'
                )
                return redirect('official-login')

            else:
                messages.error(
                    request,
                    'Your account role is not configured.'
                )

        else:
            messages.error(
                request,
                'Invalid username or password.'
            )

    return render(
        request,
        'user/cooperative.html',
        {'form': form}
    )


def farmer_login(request):
	form = AuthenticationForm()
	if request.method == 'POST':  
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		
		if user is not None:
			# Check if any user is already logged in, log them out first
			if request.user.is_authenticated:
				logout(request)
			
			if user.is_authenticated and user.is_farmer:
				login(request, user)
				return redirect('farmer-portal')
			elif user.is_authenticated and user.is_vet_officer:
				messages.warning(request, 'Kindly login as a Vet Officer')
				return redirect('vet-login')
		else:
			messages.error(request, 'Invalid Credentials')

	return render(request, 'user/farmerlogin.html', {'form': form})

def universal_login(request):
    # Define role mapping
    ROLE_MAPPING = {
        'is_farmer': {
            'redirect': 'farmer-portal',
            'name': 'Farmer',
            'login_url': 'farmer-login'
        },
        'is_vet_officer': {
            'redirect': 'vet-portal',
            'name': 'Veterinary Officer',
            'login_url': 'vet-login'
        },
        'is_official': {
            'redirect': 'official-portal',
            'name': 'Government Official',
            'login_url': 'official-login'
        },
        'is_cooperative': {
            'redirect': 'cooperative-portal',
            'name': 'Cooperative',
            'login_url': 'cooperative-login'
        }
    }
    
    # Redirect if user is already logged in
    if request.user.is_authenticated:
        return redirect_to_user_portal(request.user, request)
    
    form = AuthenticationForm()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Logout any existing session
            if request.user.is_authenticated:
                logout(request)
            
            # Login the user
            login(request, user)
            
            # Redirect to appropriate portal
            return redirect_to_user_portal(user, request)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    
    return render(request, 'user/login.html', {'form': form})

def redirect_to_user_portal(user, request):
    """Helper function to redirect based on user role"""
    # Check roles in priority order
    if hasattr(user, 'is_farmer') and user.is_farmer:
        return redirect('farmer-portal')
    elif hasattr(user, 'is_vet_officer') and user.is_vet_officer:
        return redirect('vet-portal')
    elif hasattr(user, 'is_official') and user.is_official:
        return redirect('official-portal')
    elif hasattr(user, 'is_cooperative') and user.is_cooperative:
        return redirect('cooperative-portal')
    else:
        messages.warning(request, 'Your account role is not configured. Please contact support.')
        return redirect('index')

def user_logout(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('index')