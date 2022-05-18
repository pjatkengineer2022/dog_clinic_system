import datetime
from django.db import models
from users.models import Owner
from PIL import Image

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]
YEAR_CHOICES = year_choices()

class Pet(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=70)
    race = models.CharField(max_length=70, null=True, blank=True)
    year_birth = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True)#default=datetime.date.today().year)
    avatar = models.ImageField(upload_to="pets_profile_pics", default='assets/svg/dog_avatar.svg')
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        super().save( *args, **kwargs)			
        img = Image.open(self.image.path)		 
        if img.height > 300 or img.width >300:	
            output_size= (300,300)
            img.thumbnail(output_size) 			
            img.save(self.image.path)			