from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import PatientUser,DoctorUser
from .permissions import IsPatient,IsDoctor
from .serializers import PatientUserSerializer,DoctorUserSerializer
from logging import getLogger
from .permissions import IsDoctor,IsPatient
logger = getLogger(__name__)
# Create your views here.

class PatientRegisterAPI(APIView):
    def post(self,request):
        serializer = PatientUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Patient registered successfully")
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DoctorRegisterAPI(APIView):
    def post(self,request):
        serializer=DoctorUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Doctor registered successfully")
            return Response(serializer.data,status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
