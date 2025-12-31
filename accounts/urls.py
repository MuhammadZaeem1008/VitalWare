from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
from .views import PatientRegisterAPI,DoctorRegisterAPI
urlpatterns=[
    path("login/",TokenObtainPairView.as_view() ,name="token_obtain"),
    path("api/token/refresh",TokenRefreshView.as_view(),name='token_refresh'),
    path("register/patient/",PatientRegisterAPI.as_view(),name='register'),
    path("register/doctor/",DoctorRegisterAPI.as_view(),name='register')
]