
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('admin_dashboard', admin_dashboard, name='admin_dashboard'),
    path('doctor_dashboard', doctor_dashboard, name='doctor_dashboard'),
    path('nurse_dashboard', nurse_dashboard, name='nurse_dashboard'),
    path('receptionist_dashboard', receptionist_dashboard, name='receptionist_dashboard'),
    path('manage_admit_discharge/', manage_admit_discharge, name='manage_admit_discharge'),
    path('manage_payments/', manage_payments, name='manage_payments'),
    path('success/', payment_success, name='payment_success'),
    path('cancel/', payment_cancel, name='payment_cancel'),
    path('patient_dashboard', patient_dashboard, name='patient_dashboard'),
    path('appointment/', appointment, name='appointment'),
    path('appointment/submit/', appointment_submit, name='appointment_submit'),
    path('appointment_details/<int:appointment_id>/',appointment_details, name='appointment_details'),
    path('logout/', custom_logout, name='logout'),
    path('about/', about_us, name='about_us'),
    # User URLs
    path('list_users/', list_users, name='list_users'),
    path('update_user/<int:user_id>/', update_user, name='update_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path(
        "forgate_password/",
        auth_views.PasswordResetView.as_view(
            template_name="account_reset_pass/reset_password1.html",
            success_url="/reset_password_sent/",
        ),
        name="forgate_password",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account_reset_pass/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account_reset_pass/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account_reset_pass/password_reset.html"
        ),
        name="password_reset_complete",
    ),
]