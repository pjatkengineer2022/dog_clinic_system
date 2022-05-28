from django.contrib import admin
from .models import Doctor, Shift, DoctorShift, Service
# Register your models here.
admin.site.register(Doctor)
admin.site.register(Shift)
admin.site.register(DoctorShift)
admin.site.register(Service)
