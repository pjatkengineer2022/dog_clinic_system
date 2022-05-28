from rest_framework import serializers
from doctors.models import DoctorShift, Doctor, Shift
from users.models import Profile

########### TRZECIE API

class DoctorShiftSerializer(serializers.ModelSerializer):  
    shiftStartTime = serializers.TimeField(read_only=True,source='shift.startTime')
    shiftEndTime = serializers.TimeField(read_only=True, source='shift.endTime')
    class Meta:
        model = DoctorShift
        fields = ['date', 'shiftStartTime', 'shiftEndTime']

class DoctorSerializer(serializers.ModelSerializer):
    doctorname = serializers.CharField(source='profile.name')
    doctorshift = DoctorShiftSerializer(many=True)
    class Meta:
        model = Doctor
        fields = ['id','doctorname', 'doctorshift']


########### DRUGIE API

class DoctorShiftSerializer(serializers.ModelSerializer):
    doctorname = serializers.CharField(source='doctor.profile.name')
    doctorid = serializers.CharField(source='doctor.id')
    shiftStartTime = serializers.TimeField(read_only=True,source='shift.startTime')
    shiftEndTime = serializers.TimeField(read_only=True, source='shift.endTime')
    class Meta:
        model = DoctorShift
        fields = [  'doctorid', 'doctorname', 'shiftStartTime', 'shiftEndTime','date' ]#'doctor','shift',



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
