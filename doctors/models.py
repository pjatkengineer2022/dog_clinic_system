from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from users.models import Profile
from PIL import Image
from aaConfig.validators import validate_file_size
from django.core.files.storage import default_storage as storage

class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=300)
    def __str__(self):
        return self.name

class Doctor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to="doctor_profile_pics", validators=[validate_file_size], default='doctor_avatar.png')
    service = models.ManyToManyField(Service)
    def __str__(self):
        return self.profile.user.username + ' doctor'
    def save(self, *args, **kwargs):
        super().save( *args, **kwargs)			
        img = Image.open(storage.open(self.image.name))		 
        if img.height > 300 or img.width >300:	
            output_size= (300,300)
            img.thumbnail(output_size) 			
            img.save(storage.open(self.image.name))
        group, was_created = Group.objects.get_or_create(name='doctor')
        self.profile.user.groups.add(group)

    def get_absolute_url(self):
        return reverse('single_doctor', kwargs={'pk':self.pk})

class Shift(models.Model):
    name = models.CharField(max_length=1000)
    startTime = models.TimeField(default=None)
    endTime = models.TimeField(default=None)
    def __str__(self):
        return self.name + ": "+str(self.startTime.strftime("%H:%M"))+" - "+str(self.endTime.strftime("%H:%M"))

class DoctorShift(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctorshifts')
    date = models.DateField(default=None)
    def __str__(self):
        return str(self.date) + ': '+ self.shift.name +' - '+ self.doctor.profile.name
