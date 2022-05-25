from django.db import models
from django.utils import timezone
from pets.models import Pet, Treatment
from doctors.models import Doctor
# Create your models here.

class Status(models.Model):
    STATUS = (
        ('odbyta','odbyta'),
        ('nieodbyta','nieodbyta'),
    )
    name = models.CharField(max_length=100, choices = STATUS, default='nieodbyta')

class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=100)

class Visit(models.Model):
    pet = models.ForeignKey(Pet, on_delete = models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ManyToManyField(Service)
    ownerComment = models.CharField(max_length=2000, null=True, blank=True)

class Diagnosis(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True)
    desciption = models.CharField(max_length=4000)



