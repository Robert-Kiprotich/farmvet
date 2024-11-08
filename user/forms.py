from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()

class VetOfficerSignUpForm(UserCreationForm):
	first_name = forms.CharField(
		max_length=50,
		min_length=4,
		required=True,
		widget=forms.TextInput(
				attrs={
					'placeholder': 'First Name',
					'class': 'form-control'
				}
			)
		)
	last_name = forms.CharField(
		max_length=30,
		required=True,
		widget=forms.TextInput(
				attrs={
					'placeholder': 'Last Name',
					'class': 'form-control'
				}
			)
		)
		
	email = forms.EmailField(
		max_length=254,
		widget=forms.EmailInput(
			attrs={
				'placeholder': 'Email',
				'class': 'form-control'
			}
		)
	)
	phone_number = forms.RegexField(regex='^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', max_length=13)
	specialization=forms.ChoiceField(choices=[('large', 'Large Animals'), ('small', 'Small Animals')], label='Select Specialization')
	vet_category=forms.ChoiceField(choices=[('surgeon', 'Surgeon'), ('technologist', 'Technologist'), ('technician', 'Technician')], label='Select Vet Category')
	country=forms.CharField()
	location=forms.CharField()
	registration_number=forms.CharField()
	inst_of_grad = forms.CharField(label='Institution Of Graduation')

	

	
	password1 = forms.CharField(
		label='Password',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				'placeholder': 'Password',
				'class': 'form-control'
			}
		)
	)

	password2 = forms.CharField(
		label='Confirm Password',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				'placeholder': 'Confirm Password',
				'class': 'form-control'
			}
		)
	)
	
	class Meta(UserCreationForm.Meta):
		model = User
		fields = ('username','first_name','last_name','phone_number','specialization','vet_category','country','location','registration_number','inst_of_grad','email','password1', 'password2',)

	
class FarmerSignUpForm(UserCreationForm):
	first_name = forms.CharField(
		max_length=50,
		min_length=4,
		required=True,
		widget=forms.TextInput(
				attrs={
					'placeholder': 'First Name',
					'class': 'form-control'
				}
			)
		)
	last_name = forms.CharField(
		max_length=30,
		required=True,
		widget=forms.TextInput(
				attrs={
					'placeholder': 'Last Name',
					'class': 'form-control'
				}
			)
		)
	email = forms.EmailField()
	phone_number = forms.RegexField(regex='^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', max_length=13)
	farm_name  = forms.CharField(max_length=20)
	country=forms.CharField(label='County')
	location = forms.CharField(max_length=30)
	password1 = forms.CharField(
		label='Password',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				'placeholder': 'Password',
				'class': 'form-control'
			}
		)
	)

	password2 = forms.CharField(
		label='Confirm Password',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				'placeholder': 'Confirm Password',
				'class': 'form-control'
			}
		)
	)
	
	
	
	


	class Meta(UserCreationForm.Meta):
		model = User
		fields = ['username','first_name','last_name','farm_name','email','phone_number','country', 'location','password1', 'password2']
			

class OfficialSignUpForm(UserCreationForm):
	first_name = forms.CharField(
		max_length=50,
		min_length=4,
		required=True,
		widget=forms.TextInput(
				attrs={
					'placeholder': 'First Name',
					'class': 'form-control'
				}
			)
		)
	last_name = forms.CharField(
		max_length=30,
		required=True,
		widget=forms.TextInput(
				attrs={
					'placeholder': 'Last Name',
					'class': 'form-control'
				}
			)
		)
		
	email = forms.EmailField(
		max_length=254,
		widget=forms.EmailInput(
			attrs={
				'placeholder': 'Email',
				'class': 'form-control'
			}
		)
	)
	phone_number = forms.RegexField(regex='^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', max_length=13)
	vet_category=forms.ChoiceField(choices=[('surgeon', 'Surgeon'), ('technologist', 'Technologist'), ('technician', 'Technician')], label='Select Vet Category')
	county=forms.CharField()
	sub_county=forms.CharField()
	employment_number=forms.CharField()
	designation=forms.ChoiceField(choices=[('director', 'Director'), ('svo', 'Svo')], label='Select Designation')

	

	
	password1 = forms.CharField(
		label='Password',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				'placeholder': 'Password',
				'class': 'form-control'
			}
		)
	)

	password2 = forms.CharField(
		label='Confirm Password',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				'placeholder': 'Confirm Password',
				'class': 'form-control'
			}
		)
	)
	
	class Meta(UserCreationForm.Meta):
		model = User
		fields = ('username','first_name','last_name','phone_number','vet_category','county','sub_county','registration_number','employment_number','designation','email','password1', 'password2',)

