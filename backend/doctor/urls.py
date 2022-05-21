from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from users import views as users_views, forms as users_forms



urlpatterns =[
    path('login/', auth_views.LoginView.as_view(template_name='doctors/login.html'), name='login_doctor'),
    
]