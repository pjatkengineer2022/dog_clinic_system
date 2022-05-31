from django.contrib import admin
from.models import MedicineHistory, Pet, Disease,  Producer, Medicine, Treatment, MedicineHistory
# Register your models here.
admin.site.register(Pet)
admin.site.register(Disease)
admin.site.register(Producer)
admin.site.register(Medicine)
admin.site.register(Treatment)
admin.site.register(MedicineHistory)
