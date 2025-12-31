from django.db import models
from accounts.models import DoctorUser,PatientUser
class DoctorBio(models.Model):
    DoctorUser=models.OneToOneField(DoctorUser,on_delete=models.CASCADE)
    about=models.TextField()
    experience=models.CharField()
    education=models.TextField()
    fees=models.IntegerField()


def __str__(self):
    return self.DoctorUser.user.username


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(DoctorUser, on_delete=models.CASCADE)
    start_time=models.TimeField()
    end_time=models.TimeField()
    date=models.DateField()
    created_at=models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ("doctor", "date", "start_time")

    def __str__(self):
        return f"{self.doctor.user.username} {self.date}"

class DoctorTimeSlot(models.Model):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("PENDING", "Pending"),
        ("BOOKED", "Booked"),
    ]

    doctor = models.ForeignKey(DoctorUser, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="AVAILABLE"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("doctor", "date", "start_time")



class Appointment(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("REJECTED", "Rejected"),
    ]

    patient = models.ForeignKey(PatientUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorUser, on_delete=models.CASCADE)
    slot = models.OneToOneField(DoctorTimeSlot, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    created_at = models.DateTimeField(auto_now_add=True)




