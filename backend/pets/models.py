import datetime
from django.utils import timezone
from django.db import models
from backend.users.models import Owner
from PIL import Image
from backend.aaConfig.validators import validate_file_size

def year_choices():
    return [(r,r) for r in range(datetime.date.today().year-30, datetime.date.today().year+1)]
YEAR_CHOICES = year_choices()

class Pet(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=70)
    race = models.CharField(max_length=70, null=True, blank=True)
    year_birth = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True)#default=datetime.date.today().year)
    avatar = models.ImageField(upload_to="pet_profile_pics", validators=[validate_file_size], default='dog_avatar.png')
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        super().save( *args, **kwargs)			
        img = Image.open(self.avatar.path)		 
        if img.height > 300 or img.width >300:	
            output_size= (300,300)
            img.thumbnail(output_size) 			
            img.save(self.avatar.path)	

class Disease(models.Model):
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=1000, null=True, blank=True)
    def __str__(self):
        return self.name

class Producer(models.Model):
    name = models.CharField(max_length=70)
    mail = models.EmailField(max_length=1000, null=True, blank=True)
    def __str__(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=70)
    producer = models.ForeignKey(Producer, on_delete = models.CASCADE)
    description = models.CharField(max_length=1000, null=True, blank=True)
    def __str__(self):
        return self.name

#diagnoza
class Treatment(models.Model):
    start = models.DateField(default = timezone.now)     
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.pet.owner.profile.user.username+" "+self.pet.name +" "+self.disease.name

class MedicineHistory(models.Model):
    startDate = models.DateField(default = timezone.now)  
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True, blank=True)#, related_name="medicine")
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True, blank=True)#, related_name="treatment")
    def __str__(self):
        return self.medicine.name +" "+str(self.startDate)+" - "+ self.treatment.disease.name +": "+ self.treatment.pet.name +" - "+self.treatment.pet.owner.profile.name
