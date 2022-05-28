from django.shortcuts import render
from rest_framework.generics import (ListAPIView)
#from .serializers import DoctorShiftSerializer, DoctorSerializer
from doctors.models import DoctorShift, Doctor
from datetime import datetime

# class DoctorShiftListApiView(ListAPIView):
#     serializer_class = DoctorShiftSerializer
#     queryset = DoctorShift.objects.filter(date__gte = datetime.now()).order_by('date')

# class DoctorWithShiftsListApiView(ListAPIView):
#     serializer_class = DoctorSerializer
#     queryset = Doctor.objects.all()
#     #queryset = Doctor.objects.all().exclude('doctorshift__')#filter(doctorshift__in = doctorshiftSetDate)#.order_by('doctorshift__date')
