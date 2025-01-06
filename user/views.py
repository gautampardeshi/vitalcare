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
from django.http import Http404
import stripe
from django.views.decorators.csrf import csrf_exempt

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

    # Fetch data for the dashboard
    user_roles = {
        'admins': CustomUser.objects.filter(role='admin').count(),
        'doctors': CustomUser.objects.filter(role='doctor').count(),
        'patients': CustomUser.objects.filter(role='patient').count(),
        'nurses': CustomUser.objects.filter(role='nurse').count(),
        'receptionists': CustomUser.objects.filter(role='receptionist').count(),
    }

    context = {
        'admin_name': f"{request.user.first_name} {request.user.last_name}",
        'user_roles': user_roles,
        'appointments_list': Appointment.objects.all(),
        'payments_list': Payment.objects.all(),
        'admit_discharge_list': AdmitDischargeDetails.objects.all(),
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
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.user.role != 'doctor' or appointment.doctor != request.user:
        return render(request, '403.html')  
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['pending', 'approved']:
            appointment.appointment_status = status
            appointment.save()  
            return redirect('doctor_dashboard') 
    return render(request, 'appointment_details.html', {
        'appointment': appointment
    })


# appointment view 
@login_required
def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Save the appointment
            appointment = form.save(commit=False)
            appointment.patient_email = request.user.email 
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
    if request.user.role != 'patient':  
        return render(request, '403.html') 
    appointments = Appointment.objects.filter(patient_email=request.user.email)
    print("Logged-in user email:", request.user.email) 
    print("Appointments retrieved:", appointments)
    if not appointments.exists():
        messages.info(request, "No appointments found for your account.")
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

@login_required
def manage_admit_discharge(request):
    if request.user.role != 'receptionist':
        return render(request, '403.html')  # Ensure this template exists

    if request.method == 'POST':
        form = AdmitDischargeForm(request.POST)
        if form.is_valid():
            admit_discharge = form.save()
            messages.success(request, "Admit/Discharge details saved successfully!")
            return redirect('manage_admit_discharge.html')  # Ensure this URL is defined
        else:
            messages.error(request, "There were errors in the form. Please correct them.")
    else:
        form = AdmitDischargeForm()
    return render(request, 'manage_admit_discharge.html', {'form': form})

stripe.api_key = 'sk_test_tR3PYbcVNZZ796tH88S4VQ2u'
@login_required
def manage_payments(request):
    if request.user.role != 'receptionist':
        return render(request, '403.html')  # Restrict unauthorized access

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Get and validate the total_amount field (formerly amount)
            payment = form.save(commit=False)
            total_amount = payment.total_amount  # Use total_amount instead of amount
            if total_amount <= 0:
                messages.error(request, "Invalid total amount. Must be greater than zero.")
                return redirect('manage_payments')

            # Save the payment details
            payment.save()

            # Create a Stripe Checkout session
            try:
                YOUR_DOMAIN = 'http://127.0.0.1:8000'  # Replace with your domain
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'inr',
                                'product_data': {
                                    'name': 'Total amount',
                                },
                                'unit_amount': int(total_amount * 100),  # Convert to smallest currency unit
                            },
                            'quantity': 1,
                        },
                    ],
                    mode='payment',
                    success_url=f"{YOUR_DOMAIN}/success/",
                    cancel_url=f"{YOUR_DOMAIN}/cancel/",
                )
                # Redirect to the Stripe Checkout URL
                return redirect(checkout_session.url)
            except stripe.error.StripeError as e:
                messages.error(request, f"Stripe error: {str(e)}")
            except Exception as e:
                messages.error(request, f"Unexpected error: {str(e)}")
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = PaymentForm()

    return render(request, 'manage_payments.html', {'form': form})

def payment_success(request):
    return render(request, 'success.html')  # Create a success.html template

def payment_cancel(request):
    return render(request, 'cancel.html')

# List all users
@login_required
def list_users(request):
    if request.user.role != 'admin':
        return render(request, '403.html')  # Unauthorized access
    users = CustomUser.objects.all()
    return render(request, 'list_users.html', {'users': users})

# Update user details
@login_required
def update_user(request, user_id):
    if request.user.role != 'admin':
        return render(request, '403.html')  # Unauthorized access
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = RoleBasedUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('list_users')
    else:
        form = RoleBasedUserCreationForm(instance=user)

    return render(request, 'update_user.html', {'form': form, 'user': user})


# Delete user
@login_required
def delete_user(request, user_id):
    if request.user.role != 'admin':
        return render(request, '403.html')  # Unauthorized access
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        user.delete()
        return redirect('list_users')  # Redirect after deletion
    
    return render(request, 'delete_user.html', {'user': user})

