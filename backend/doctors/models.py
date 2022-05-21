from django.db import models
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
