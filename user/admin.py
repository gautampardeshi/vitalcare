
# Register your models here.
from django.contrib import admin
from .models import (
    CustomUser,Appointment,Payment,AdmitDischargeDetails
)
# user creation field 
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'email', 'DEPARTMENT','first_name','last_name')
    search_fields = ('username', 'role', 'email')
    list_filter = ('role', 'is_staff', 'is_active')

  
# Appointment Details
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'patient_name', 
        'patient_age', 
        'appointment_date',
        'patient_contact_number',
        'purpose_of_visit',
        'symptoms',
        'appointment_status',
    ]

@admin.register(AdmitDischargeDetails)
class AdmitDischargeDetailsAdmin(admin.ModelAdmin):
    list_display = ['patient','doctor', 'admit_date', 'discharge_date']
    search_fields = ['patient__first_name', 'patient__last_name']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'total_amount', 'payment_date']
    list_filter = ['payment_date']
    search_fields = ['patient__first_name', 'patient__last_name']

