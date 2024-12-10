# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('nurse', 'Nurse'),
        ('receptionist', 'Receptionist'),
    ]
    GENDER_CHOICE=[
        ('MALE','MALE'),
        ('FEMALE','FEMALE')
    ]
    DEPARTMENT_CHOICES=[
        ('emergency', 'Emergency'),
        ('opd', 'Outpatient Department (OPD)'),
        ('surgery', 'Surgery'),
        ('radiology', 'Radiology'),
        ('laboratory', 'Laboratory'),
        ('pediatrics', 'Pediatrics'),
        ('gynecology', 'Gynecology & Obstetrics'),
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('dermatology', 'Dermatology'),
        ('psychiatry', 'Psychiatry & Mental Health'),
        ('ophthalmology', 'Ophthalmology'),
        ('pharmacy', 'Pharmacy'),
        ('orthopedics', 'Orthopedics'),
        ('nephrology', 'Nephrology'),
        ('urology', 'Urology'),
        ('gastroenterology', 'Gastroenterology'),
        ('infectious_diseases', 'Infectious Diseases')
    ]
    DEPARTMENT = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, default="general")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICE, null=True, blank=True)
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    
#appointment
class Appointment(models.Model):
    GENDER_CHOICE = [
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE')
    ]
    PURPOSE_OF_VISIT = [
        ('consultation', 'Consultation'),
        ('emergency', 'Emergency'),
        ('diagnosis', 'Diagnosis/Tests'),
        ('treatment', 'Treatment'),
        ('surgery', 'Surgery'),
        ('vaccination', 'Vaccination'),
        ('others', 'Others'),
    ]
    
    doctor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'doctor'},
        related_name='appointments'
    ) 
    patient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'},
        related_name='patient_appointments',
        null=True,
        blank=True
    )  # Relationship with patient
    patient_name = models.CharField(max_length=200)
    patient_age = models.IntegerField()
    appointment_date = models.DateField(default=date.today)
    patient_gender = models.CharField(max_length=10, choices=GENDER_CHOICE)
    patient_contact_number = models.CharField(max_length=15)
    patient_email = models.EmailField()
    purpose_of_visit = models.CharField(max_length=70, choices=PURPOSE_OF_VISIT)
    symptoms = models.TextField(blank=True, null=True)
    appointment_status = models.CharField(
        max_length=20,
        choices=[('approved', 'Approved'), ('pending', 'Pending')],
        default='Pending'
    )
    payment = models.OneToOneField(
        'Payment', 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='appointment_payment'
    )  # Optional relationship with Payment

    def __str__(self):
        return f"Appointment for {self.patient_name} with Dr. {self.doctor.get_full_name()} on {self.appointment_date}"

    def save(self, *args, **kwargs):
        if self.pk:  # Check if this is an update
            original = Appointment.objects.get(pk=self.pk)
            if original.appointment_status != self.appointment_status:
                print(f"Appointment status changed from {original.appointment_status} to {self.appointment_status}")
        super().save(*args, **kwargs)

class AdmitDischargeDetails(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'patient'})
    admit_date = models.DateField(null=True,blank=True,default=date.today)
    discharge_date = models.DateField(null=True, blank=True,default=date.today)
    discharge_summary = models.TextField(null=True, blank=True)
    ward = models.CharField(max_length=100, null=True, blank=True)  # Ward details
    treatment_plan = models.TextField(null=True, blank=True)  # Treatment plan details

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} - Admit: {self.admit_date}, Discharge: {self.discharge_date or 'N/A'}"


class Payment(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'patient'},null=True, blank=True)  # Relationship with CustomUser
    admit_discharge_details = models.ForeignKey(AdmitDischargeDetails, on_delete=models.SET_NULL, null=True, blank=True)  # Link with AdmitDischargeDetails
    admit_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    consultancy_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(default=date.today)

    def save(self, *args, **kwargs):
        # Automatically calculate the total amount
        self.total_amount = self.admit_charges + self.consultancy_fees + self.other_charges
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for {self.patient.first_name} {self.patient.last_name} - Total: {self.total_amount}"