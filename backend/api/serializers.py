from pets.models import Pet
from rest_framework import serializers
from doctors.models import DoctorShift, Doctor, Shift
from visits.models import Visit
from users.models import Profile



########### TRZECIE (Właściwe) API
class VisitSerializer(serializers.ModelSerializer):#track
    petId = serializers.CharField(source='pet.id')
    petName = serializers.CharField(source='pet.name')
    class Meta:
        model = Visit
        fields = ['date', 'petId', 'petName']        

class DoctorShiftSerializer(serializers.ModelSerializer):  
    shiftStartTime = serializers.TimeField(read_only=True,source='shift.startTime')
    shiftEndTime = serializers.TimeField(read_only=True, source='shift.endTime')
    class Meta:
        model = DoctorShift
        fields = ['date', 'shiftStartTime', 'shiftEndTime']

class DoctorSerializer(serializers.ModelSerializer):#album
    doctorname = serializers.CharField(source='profile.name')
    doctorshifts = DoctorShiftSerializer(many=True)
    visits = VisitSerializer(many=True)
    class Meta:
        model = Doctor
        fields = ['id','doctorname', 'doctorshifts', 'visits']


# ########## DRUGIE API

# class DoctorShiftSerializer(serializers.ModelSerializer):
#     doctorname = serializers.CharField(source='doctor.profile.name')
#     doctorid = serializers.CharField(source='doctor.id')
#     shiftStartTime = serializers.TimeField(read_only=True,source='shift.startTime')
#     shiftEndTime = serializers.TimeField(read_only=True, source='shift.endTime')
#     class Meta:
#         model = DoctorShift
#         fields = [  'doctorid', 'doctorname', 'shiftStartTime', 'shiftEndTime','date' ]#'doctor','shift',



########### PIERWSZE API

# class DoctorSerializer(serializers.ModelSerializer):
#     doctorname = serializers.CharField(source='profile.name')
#     class Meta:
#         model = Doctor
#         fields = ['id','doctorname']

# class ShiftSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Shift
#         fields = ['name', 'startTime', 'endTime']

# class DoctorShiftSerializer(serializers.ModelSerializer):
#     doctor = DoctorSerializer()
#     shift = ShiftSerializer()
#     class Meta:
#         model = DoctorShift
#         fields = ['doctor','shift', 'date']
