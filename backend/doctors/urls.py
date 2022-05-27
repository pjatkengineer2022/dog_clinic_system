from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from users import views as users_views



urlpatterns =[
    #path('login/', auth_views.LoginView.as_view(template_name='doctors/doctor_login.html'), name='login_doctor'),
    path('login/', views.loginDoctor, name='login_doctor'),
    path('logout/', users_views.logoutUser, name='logout_doctor'),
    path('', views.DoctorList.as_view(), name='doctors'),
    path('doctor/<pk>/', views.SingleDoctorDetail.as_view(), name='single_doctor'),
    # path('doctor_browse_patients/', views.DoctorBrowsePatientListView.as_view(), name='doctor_browse_patients'),
    path('doctor_browse_patients/', views.doctor_browse_patients, name='doctor_browse_patients'),
    path('diseases_history/<int:id>/', views.dog_diseases_history_list, name='diseases_history'),
    path('medicines_history/<int:id>/', views.dog_medicines_history_list, name='medicines_history'),
    path('visits_history/<int:id>/', views.dog_visits_history_list, name='dog_history_visits'),
    path('doctor_check_visits/', views.doctor_check_visits_list, name='doctor_check_visits'),
    path('add_medicines/', views.add_medicines, name='add_medicines'),
    path('add_doctor_shift/', views.add_doctor_shift, name='add_doctor_shift'),
    path('remove_doctor_shift/<int:id>/',views.remove_doctor_shift, name='remove_doctor_shift'),
    path('doctor_shift_list/',views.doctor_shift_list, name='doctor_shift_list'),
]
