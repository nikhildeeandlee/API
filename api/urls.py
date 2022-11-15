from . import views
from django.urls import path
from django.urls import re_path as url

urlpatterns = [
    url(r'^patient/register$', views.patient_register, name="patient-register"),
    url(r'^patient/login$', views.patient_login),
    path('patient/display/<int:id>', views.patient_display),
    path('patient/update/<int:id>', views.patient_update),

    path(
        "reset-password/",
        views.PasswordReset.as_view(),
        name="reset-password",
    ),
    path(
        "change-password/<str:encoded_pk>/<str:token>/",
        views.ChangePassword.as_view(),
        name="reset-password",
    ),


    path(
        "reset-password-doctor/",
        views.PasswordResetDoctor.as_view(),
        name="reset-password-doctor",
    ),
    path(
        "change-password-doctor/<str:encoded_pk>/<str:token>/",
        views.ChangePasswordDoctor.as_view(),
        name="reset-password-doctor",
    ),


    path('verify/<auth_token>', views.verify, name="verify"),
    path('doctor-verify/<auth_token>', views.doctor_verify, name="doctor_verify"),


    url(r'^tech/register$', views.tech_register),
    url(r'^tech/login$', views.tech_login),
    url(r'^tech/display$', views.tech_display),


    url(r'^doctor/register$', views.doctor_register),
    url(r'^doctor/login$', views.doctor_login),
    path('doctor/display/<int:id>', views.doctor_display),


    path('pain-selection/<int:id>', views.pain_selection),
    path('pain-details/<int:id>', views.pain_details),


    path('present-pain-pattern/<int:id>',
         views.present_pain_pattern, name="present_pain_pattern"),
    path('pain-investigation/<int:id>',
         views.pain_investigation, name="pain_investigation"),
    path('pain-investigation-checkbox/<int:id>',
         views.pain_investigation_checkbox, name="pain_investigation_checkbox"),


    path('regular-medication/<int:id>',
         views.regular_medication, name="regular_medication"),


    path('pain-other-effect-checkbox/<int:id>',
         views.pain_other_effect_checkbox, name="pain_other_effect_checkbox"),
    path('pain-other-effect/<int:id>',
         views.pain_other_effect, name="pain_other_effect"),


    path('personal-details/<int:id>', views.personal_details, name="personal_details"),
    path('personal-details-checkbox/<int:id>', views.personal_details_checkbox, name="personal_details_checkbox"),
]
