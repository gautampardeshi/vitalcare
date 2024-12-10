from .models import CustomUser,Appointment
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RoleBasedUserCreationForm,AuthenticationForm
from django.contrib import messages
from .forms import AppointmentForm
from datetime import date
from django.contrib.auth import logout
from .models import AdmitDischargeDetails, Payment, Appointment
from .forms import AdmitDischargeForm, PaymentForm

# ye home vala hai 
def home_view(request):
    return render(request, 'home.html')

# yee vala registration vala hai 
def signup_view(request):
    if request.method == 'POST':
        form = RoleBasedUserCreationForm(request.POST)
        if form.is_valid():
            print("Form is valid, saving data...")
            form.save()  # Save the user or perform your own logic
            return redirect('login')  # Redirect to a success page or another page
        else:
            print("Form errors:", form.errors)  # Debug: Print errors if form is not valid
    else:
        form = RoleBasedUserCreationForm()
    return render(request, 'signup.html', {'form': form})

# yee login vala hai 
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'doctor':
                    return redirect('doctor_dashboard')
                elif user.role == 'nurse':
                    return redirect('nurse_dashboard')
                elif user.role == 'receptionist':
                    return redirect('receptionist_dashboard')
                elif user.role == 'patient':
                    return redirect('patient_dashboard')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# ye logout ka hai 
def custom_logout(request):
    logout(request)
    return render(request, 'logout_success.html')

@login_required
def admin_dashboard(request):
    # Check if the logged-in user is an admin
    if request.user.role != 'admin':
        return render(request, '403.html')  # Unauthorized access

    # Get the data to be displayed
    user_roles = {
        'admins': CustomUser.objects.filter(role='admin'),
        'doctors': CustomUser.objects.filter(role='doctor'),
        'patients': CustomUser.objects.filter(role='patient'),
        'nurses': CustomUser.objects.filter(role='nurse'),
        'receptionists': CustomUser.objects.filter(role='receptionist'),
    }

    # Appointments, payments, and admits are displayed
    context = {
        'admin_name': f"{request.user.first_name} {request.user.last_name}",
        'user_roles': user_roles,
        'appointments': Appointment.objects.all(),
        'payments': Payment.objects.all(),
        'admits': AdmitDischargeDetails.objects.all(),
    }

    return render(request, 'admin_dashboard.html', context)


# yee doctor logic
@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return render(request, '403.html')  # Unauthorized access

    # Fetch appointments assigned to the logged-in doctor
    appointments = Appointment.objects.filter(doctor=request.user)
    return render(request, 'doctor_dashboard.html', {'appointments': appointments})

# appointment vala hai 

@login_required
def appointment_details(request, appointment_id):
    # Fetch the appointment or return 404 if not found
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Ensure the logged-in user is a doctor and assigned to this appointment
    if request.user.role != 'doctor' or appointment.doctor != request.user:
        return render(request, '403.html')  # Unauthorized access

    if request.method == 'POST':
        # Fetch the new status from the POST data
        status = request.POST.get('status')
        # Validate the status before updating
        if status in ['pending', 'approved']:
            appointment.appointment_status = status
            appointment.save()  # Save the updated status
            return redirect('doctor_dashboard')  # Redirect to the doctor dashboard

    # If GET request, render the appointment details template
    return render(request, 'appointment_details.html', {
        'appointment': appointment
    })


# appointment view 
@login_required
def appointment_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Save the appointment
            appointment = form.save(commit=False)
            appointment.patient_email = request.user.email  # Link logged-in patient email
            appointment.save()
            return redirect('appointment_submit')
    else:
        form = AppointmentForm()
    return render(request, 'appointment.html', {'form': form})

# appointment submit ka hai yee
def appointment_submit(request):
    return render(request, 'appointment_submission_success.html')

# yee nurse ka hai 
@login_required
def nurse_dashboard(request):
    return render(request, 'nurse_dashboard.html')

# views.py
@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':  # Ensure only patients access this view
        return render(request, '403.html')  # Unauthorized access
    appointments = Appointment.objects.filter(patient_email=request.user.email)
    return render(request, 'patient_dashboard.html', {'appointments': appointments})


# yee mene about us valii hai 
def about_us(request):
    return render(request, 'about_us.html')


# receptionist ke liye hai
@login_required
def receptionist_dashboard(request):
    if request.user.role != 'receptionist':
        return render(request, '403.html')

    appointments = Appointment.objects.all()
    admits = AdmitDischargeDetails.objects.all()
    payments = Payment.objects.all()

    return render(request, 'receptionist_dashboard.html', {
        'appointments': appointments,
        'admits': admits,
        'payments': payments,
    })

# views.py (Update)

@login_required
def manage_admit_discharge(request):
    if request.user.role != 'receptionist':
        return render(request, '403.html')

    if request.method == 'POST':
        form = AdmitDischargeForm(request.POST)
        if form.is_valid():
            admit_discharge = form.save()

            # Create a payment record for the patient
            Payment.objects.create(
                patient=admit_discharge.patient,
                amount=0.0,  # Adjust as needed
                payment_date=date.today(),
                status='pending'  # Ensure this matches a valid choice in the model
            )

            return redirect('receptionist_dashboard')
    else:
        form = AdmitDischargeForm()

    return render(request, 'manage_admit_discharge.html', {'form': form})


@login_required
def manage_payments(request):
    if request.user.role != 'receptionist':
        return render(request, '403.html')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('receptionist_dashboard')
    else:
        form = PaymentForm()
    return render(request, 'manage_payments.html', {'form': form})




