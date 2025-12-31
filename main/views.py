from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from accounts.permissions import IsDoctor
from rest_framework.response import Response
from rest_framework import status
from .models import DoctorBio, Appointment, DoctorTimeSlot
from .serializers import DoctorBioSerializer, AppointmentRequestSerializer, DoctorTimeSlotSerializer, \
    DoctorAvailabilitySerializer
from logging import getLogger

from accounts.permissions import IsPatient

from accounts.models import DoctorUser

logger = getLogger(__name__)

class DoctorBioView(APIView):
    permission_classes = [IsAuthenticated,IsDoctor]
    def post(self,request):
        print("user is ",request.user)
        print("user is doctor with data", request.data)
        serializer_class = DoctorBioSerializer(data=request.data,context={'request':request})
        if serializer_class.is_valid():
            serializer_class.save()
            logger.info("Doctor bio created successfully")
            return Response(serializer_class.data,status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        doctor_bio=DoctorBio.objects.get(DoctorUser=request.user.doctoruser)
        serializer_class = DoctorBioSerializer(doctor_bio)
        return Response(serializer_class.data,status=status.HTTP_200_OK)



class DoctorAvailabilityCreateAPI(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def post(self, request):
        serializer = DoctorAvailabilitySerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Availability & slots created"}, status=201)




class DoctorAvailableSlotsAPI(APIView):
    def get(self, request, doctor_id):
        date = request.GET.get("date")
        doctor=DoctorUser.objects.get(id=doctor_id)
        slots = DoctorTimeSlot.objects.filter(
            doctor=doctor,
            date=date,
            status="AVAILABLE"
        )
        print(slots)
        print(doctor.user.username)
        serializer = DoctorTimeSlotSerializer(slots, many=True)
        return Response(serializer.data)






class AppointmentRequestAPI(APIView):
    permission_classes = [IsAuthenticated, IsPatient]

    def post(self, request):
        serializer = AppointmentRequestSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()
        return Response(
            {"message": "Appointment request sent", "id": appointment.id},
            status=201
        )





class AppointmentDecisionAPI(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def post(self, request, appointment_id):
        action = request.data.get("action")  # approve / reject
        appointment = Appointment.objects.get(id=appointment_id)

        if appointment.doctor != request.user.doctoruser:
            return Response({"error": "Not allowed"}, status=403)

        if action == "approve":
            appointment.status = "CONFIRMED"
            appointment.slot.status = "BOOKED"
            appointment.slot.save()

        elif action == "reject":
            appointment.status = "REJECTED"
            appointment.slot.status = "AVAILABLE"
            appointment.slot.save()

        appointment.save()
        return Response({"message": f"Appointment {action}ed"})
