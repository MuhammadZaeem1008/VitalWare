from django.urls import path
from .views import *

urlpatterns=[
    path("doctor/bio/",DoctorBioView.as_view(),name="doctor_bio"),
    path("doctor/availability/", DoctorAvailabilityCreateAPI.as_view()),
    path("doctor/<int:doctor_id>/slots/", DoctorAvailableSlotsAPI.as_view()),
    path("appointments/request/", AppointmentRequestAPI.as_view()),
    path("appointments/<int:appointment_id>/decision/", AppointmentDecisionAPI.as_view()),
]
