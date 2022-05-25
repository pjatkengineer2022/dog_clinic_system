from django.contrib import messages
from django.contrib.auth import views as auth_views, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from doctors.models import Doctor
from pets.models import Pet, Medicine, Treatment
from users.forms import UserAuthenticationForm

class DoctorList(ListView):
    model = Doctor
    template_name = 'doctors/doctors.html'
    context_object_name = 'doctors'
    paginate_by = 8

class SingleDoctorDetail(DetailView):
    model = Doctor
    template_name = 'doctors/single_doctor.html'
    context_object_name = 'doctor'


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

class DoctorBrowsePatientListView(LoginRequiredMixin, ListView):
    model=Pet
    template_name = 'doctors/doctor_browse_patients.html'
    context_object_name = 'pets'
    paginate_by = 2
    login_url = 'login_doctor'


@login_required(login_url='login_doctor')
def dog_diseases_history_list(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except:
        messages.error(request, 'dog is not exist')
        return redirect('doctor_browse_patients')
    treatments = pet.treatment_set.all()
    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(treatments, 2) # 5 users per page
    try:
        treatments = paginator.get_page(page)
    except PageNotAnInteger:
        treatments = paginator.page(1)
    except EmptyPage:
        treatments = paginator.page(1)
    context={'treatments':treatments, 'pet': pet}
    return render(request, 'doctors/disease_history.html', context)

@login_required(login_url='login_doctor')
def dog_medicines_history_list(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except:
        messages.error(request, 'dog is not exist')
        return redirect('doctor_browse_patients')
    treatments = pet.treatment_set.all()
    medicines = Medicine.objects.all()
    #dog_medicines = [medicine if medicine in treatment.medicine.all() else None for medicine in medicines for treatment in treatments]
    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(treatments, 2) # 5 users per page
    try:
        treatments = paginator.get_page(page)
    except PageNotAnInteger:
        treatments = paginator.page(1)
    except EmptyPage:
        treatments = paginator.page(1)
    context={'treatments':treatments, 'medicines':medicines, 'pet':pet}
    return render(request, 'doctors/medicines_history.html', context)