from django.db import models
from django.contrib.auth.models import User

class PatientUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    phone_number=models.IntegerField()

    def __str__(self):
        return self.user.username

class DoctorUser(models.Model):

    SPECIALIZATION_CHOICES = [
        ('general_physician', 'General Physician'),
        ('cardiologist', 'Cardiologist'),
        ('dermatologist', 'Dermatologist'),
        ('neurologist', 'Neurologist'),
        ('orthopedic', 'Orthopedic Surgeon'),
        ('gynecologist', 'Gynecologist'),
        ('pediatrician', 'Pediatrician'),
        ('psychiatrist', 'Psychiatrist'),
        ('ent', 'ENT Specialist'),
        ('ophthalmologist', 'Ophthalmologist'),
        ('dentist', 'Dentist'),
        ('urologist', 'Urologist'),
        ('nephrologist', 'Nephrologist'),
        ('gastroenterologist', 'Gastroenterologist'),
        ('endocrinologist', 'Endocrinologist'),
    ]

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    specialization = models.CharField(
        max_length=50,
        choices=SPECIALIZATION_CHOICES
    )
    license_number = models.CharField(max_length=100)
    phone_number=models.IntegerField()
    def __str__(self):
        return self.user.username

