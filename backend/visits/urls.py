from django.urls import path
from . import views
urlpatterns = [
    path('add_diagnosis/<int:visitid>/',views.add_diagnosis, name='add_diagnosis'),
    path('add_diagnosis_no_visit/<int:petid>/',views.add_diagnosis_no_visit, name='add_diagnosis_no_visit'),
    path('doctor_add_visit/',views.doctor_book_visit_no_patient, name='doctor_add_visit'),
    path('owner_add_visit/',views.owner_book_visit_no_patient, name='owner_add_visit'),
    path('doctor_add_visit_patient/<int:petid>/',views.doctor_book_visit_with_patient, name='doctor_add_visit_patient'),
    path('owner_add_visit_patient/<int:petid>/',views.owner_book_visit_with_patient, name='owner_add_visit_patient'),
]