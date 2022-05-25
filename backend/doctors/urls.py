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
    path('doctor_browse_patients/', views.DoctorBrowsePatientListView.as_view(), name='doctor_browse_patients'),
    path('diseases_history/<int:id>/', views.dog_diseases_history_list, name='diseases_history'),
    path('medicines_history/<int:id>/', views.dog_medicines_history_list, name='medicines_history'),

]