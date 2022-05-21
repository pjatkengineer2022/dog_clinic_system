from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from users import views as users_views



urlpatterns =[
    #path('login/', auth_views.LoginView.as_view(template_name='doctors/doctor_login.html'), name='login_doctor'),
    path('login/', views.loginDoctor, name='login_doctor'),
    path('logout/', users_views.logoutUser, name='logout_doctor'),
    path('doctors/', views.DoctorList.as_view(), name='doctors'),
    path('doctor_browse_patients/', views.DoctorBrowsePatientList.as_view(), name='doctor_browse_patients'),

]