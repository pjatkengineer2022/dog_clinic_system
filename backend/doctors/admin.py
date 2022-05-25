from django.contrib import admin
from .models import Doctor, Shift, DoctorShift
# Register your models here.
admin.site.register(Doctor)
admin.site.register(Shift)
admin.site.register(DoctorShift)
