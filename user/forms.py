
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser
from .models import Appointment
from .models import AdmitDischargeDetails, Payment

class RoleBasedUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'password1', 'password2', 'role', 
            'first_name','last_name', 'contact_number', 'age', 'email', 
            'DEPARTMENT', 'gender'
        )

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'doctor',
            'patient',
            'patient_name', 
            'patient_age', 
            'appointment_date',
            'patient_gender', 
            'patient_contact_number',
            'patient_email',
            'purpose_of_visit',
            'symptoms',
            'payment',
        ]

class AdmitDischargeForm(forms.ModelForm):
    class Meta:
        model = AdmitDischargeDetails
        fields = ['patient','doctor', 'admit_date', 'discharge_date', 'discharge_summary', 'ward', 'treatment_plan']
        widgets = {
            'admit_date': forms.DateInput(attrs={'type': 'date'}),
            'discharge_date':forms.DateInput(attrs={'type':'date'})
            }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['patient', 'admit_discharge_details','admit_charges', 'consultancy_fees', 'other_charges','total_amount','payment_date']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
        }