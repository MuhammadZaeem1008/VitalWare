from datetime import datetime, timedelta

from rest_framework import serializers
from .models import DoctorBio, DoctorAvailability, DoctorTimeSlot, Appointment


class DoctorBioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorBio
        fields = ['about', 'experience', 'education', 'fees']

    def create(self, validated_data):
        doctor = self.context['request'].user.doctoruser
        print("doctor is ",doctor)
        if hasattr(doctor, 'bio'):
            raise serializers.ValidationError("Bio already exists")
        return DoctorBio.objects.create(
            DoctorUser=doctor,
            **validated_data
        )


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = ["date", "start_time", "end_time"]

    def create(self, validated_data):
        doctor = self.context["request"].user.doctoruser
        availability = DoctorAvailability.objects.create(
            doctor=doctor,
            **validated_data
        )

        start_dt = datetime.combine(
            availability.date, availability.start_time
        )
        end_dt = datetime.combine(
            availability.date, availability.end_time
        )

        slots = []
        while start_dt + timedelta(minutes=30) <= end_dt:
            slots.append(
                DoctorTimeSlot(
                    doctor=doctor,
                    date=availability.date,
                    start_time=start_dt.time(),
                    end_time=(start_dt + timedelta(minutes=30)).time()
                )
            )
            start_dt += timedelta(minutes=30)

        DoctorTimeSlot.objects.bulk_create(slots)
        return availability




class DoctorTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorTimeSlot
        fields = ["id","doctor", "date", "start_time", "end_time", "status"]


from django.db import transaction
from rest_framework.exceptions import ValidationError





class AppointmentRequestSerializer(serializers.Serializer):
    slot_id = serializers.IntegerField()

    def create(self, validated_data):
        patient = self.context["request"].user.patientuser

        with transaction.atomic():
            slot = DoctorTimeSlot.objects.select_for_update().get(
                doctor=validated_data["doctor_id"],
                date=validated_data["date"],
                start_time=validated_data["start_time"],
            )

            if slot.status != "AVAILABLE":
                raise ValidationError("Slot not available")

            slot.status = "PENDING"
            slot.save()

            return Appointment.objects.create(
                patient=patient,
                doctor=slot.doctor,
                slot=slot,
                status="PENDING"
            )
