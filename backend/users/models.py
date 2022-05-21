from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60, unique=False, null=False)
    mobileNumber = PhoneNumberField(unique=False, null=False)
    def __str__(self):
        return self.user.username + " profile"


class Owner(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return self.profile.user.username +' owner'