from django.contrib import admin
from .models import Status, Service, Diagnosis, Visit
# Register your models here.
admin.site.register(Visit)
admin.site.register(Status)
admin.site.register(Service)
admin.site.register(Diagnosis)