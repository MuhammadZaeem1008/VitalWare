from rest_framework.permissions import BasePermission
from .models import DoctorUser, PatientUser

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and DoctorUser.objects.filter(user=request.user).exists()

class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and PatientUser.objects.filter(user=request.user).exists()
