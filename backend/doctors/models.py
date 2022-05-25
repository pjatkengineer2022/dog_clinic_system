from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from users.models import Profile
from PIL import Image

class Doctor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to="doctor_profile_pics", default='doctor_avatar.png')
    def __str__(self):
        return self.profile.user.username + ' doctor'
    def save(self, *args, **kwargs):
        super().save( *args, **kwargs)			
        img = Image.open(self.image.path)		 
        if img.height > 300 or img.width >300:	
            output_size= (300,300)
            img.thumbnail(output_size) 			
            img.save(self.image.path)
        group, was_created = Group.objects.get_or_create(name='doctor')
        self.profile.user.groups.add(group)

    def get_absolute_url(self):
        return reverse('single_doctor', kwargs={'pk':self.pk})

class Shift(models.Model):
    name = models.CharField(max_length=1000)
    startTime = models.TimeField(default=None)
    endTime = models.TimeField(default=None)
    def __str__(self):
        return self.name

class DoctorShift(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(default=None)
    def __str__(self):
        return str(self.date) + ': '+ self.shift.name +' - '+ self.doctor.profile.name