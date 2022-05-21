from django.contrib import messages
from django.contrib.auth import views as auth_views, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView
from doctors.models import Doctor
from pets.models import Pet
from users.forms import UserAuthenticationForm


def loginDoctor(request):
    if not request.user.is_authenticated:
        form= UserAuthenticationForm()
        if request.method == "POST":
            form = UserAuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()                 
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('home')#zmienić doctor_browse_patient
            else:
                messages.error(request, 'Zła nazwa użytkownika lub hasło')
        context={'form':form}
        return render(request, "users/login.html", context)
    else:
        return redirect('home')

class DoctorList(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'doctors/doctors.html'
    context_object_name = 'doctors'

class DoctorBrowsePatientList(LoginRequiredMixin, ListView):
    model=Pet
    template_name = 'doctors/doctor_browse_patients.html'
    context_object_name = 'pets'

