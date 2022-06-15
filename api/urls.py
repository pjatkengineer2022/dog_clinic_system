from django.urls import path
from .views import DoctorWithShiftsListApiView # DoctorShiftListApiView,

urlpatterns = [
    path('doctor_with_shift_list',DoctorWithShiftsListApiView.as_view()),
    # path('shift_list',DoctorShiftListApiView.as_view()),
]