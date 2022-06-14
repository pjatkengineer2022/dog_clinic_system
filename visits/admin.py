from django.contrib import admin
from .models import Status, Diagnosis, Visit
# Register your models here.
admin.site.register(Visit)
admin.site.register(Status)
admin.site.register(Diagnosis)