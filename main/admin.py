from django.contrib import admin
from .models import DoctorBio,DoctorAvailability,DoctorTimeSlot,Appointment
admin.site.register(DoctorBio)
admin.site.register(DoctorAvailability)
admin.site.register(DoctorTimeSlot)
admin.site.register(Appointment)

