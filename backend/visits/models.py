from django.db import models
from django.utils import timezone
from backend.pets.models import Pet, Treatment
from doctors.models import Doctor
# Create your models here.

class Status(models.Model):
    STATUS = (
        ('odbyta','odbyta'),
        ('nieodbyta','nieodbyta'),
        ('anulowane','anulowana')
    )
    name = models.CharField(max_length=100, choices = STATUS, default='nieodbyta', unique=True)
    def __str__(self):
        return self.name

class Visit(models.Model):
    pet = models.ForeignKey(Pet, on_delete = models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='visits')
    date = models.DateTimeField(default=timezone.now)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    ownerComment = models.CharField(max_length=2000, null=True, blank=True)
    def __str__(self):
        return str(self.date) + " : " + self.pet.name

class Diagnosis(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=4000, null=True, blank=True)
    def __str__(self):
        return "visit: "+ str(self.visit.date.date()) +"; treatment: "+ self.treatment.disease.name+", "+ self.treatment.pet.name+", "+self.treatment.pet.owner.profile.name 



