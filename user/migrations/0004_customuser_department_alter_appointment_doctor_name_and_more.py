# Generated by Django 5.1.3 on 2024-11-29 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_appointment_doctor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='DEPARTMENT',
            field=models.CharField(choices=[('emergency', 'Emergency'), ('opd', 'Outpatient Department (OPD)'), ('ipd', 'Inpatient Department (IPD)'), ('surgery', 'Surgery'), ('radiology', 'Radiology'), ('laboratory', 'Laboratory'), ('pediatrics', 'Pediatrics'), ('gynecology', 'Gynecology & Obstetrics'), ('cardiology', 'Cardiology'), ('neurology', 'Neurology'), ('dermatology', 'Dermatology'), ('psychiatry', 'Psychiatry & Mental Health'), ('ophthalmology', 'Ophthalmology'), ('pharmacy', 'Pharmacy'), ('orthopedics', 'Orthopedics'), ('nephrology', 'Nephrology'), ('urology', 'Urology'), ('gastroenterology', 'Gastroenterology'), ('infectious_diseases', 'Infectious Diseases')], default='general', max_length=100),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctor_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='patient_gender',
            field=models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], max_length=10),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='purpose_of_visit',
            field=models.CharField(choices=[('consultation', 'Consultation'), ('emergency', 'Emergency'), ('diagnosis', 'Diagnosis/Tests'), ('treatment', 'Treatment'), ('surgery', 'Surgery'), ('vaccination', 'Vaccination'), ('others', 'Others')], max_length=70),
        ),
    ]
