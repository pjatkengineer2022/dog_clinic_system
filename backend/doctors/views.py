from datetime import date
from django.contrib import messages
from django.contrib.auth import views as auth_views, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q	
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from doctors.models import Doctor
from pets.models import Pet, Medicine, Treatment
from visits.models import Visit
from .forms import MedicineCreationForm, DoctorShiftCreationForm
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
                    return redirect('doctor_check_visits')
            else:
                messages.error(request, 'Zła nazwa użytkownika lub hasło')
        context={'form':form}
        return render(request, "users/login.html", context)
    else:
        return redirect('home')

# class DoctorBrowsePatientListView(LoginRequiredMixin, ListView):
#     model=Pet
#     template_name = 'doctors/doctor_browse_patients.html'
#     context_object_name = 'pets'
#     paginate_by = 2
#     login_url = 'login_doctor'
@login_required(login_url='login_doctor')
def doctor_browse_patients(request):
    pets = Pet.objects.all()
    #paginations
    page = request.GET.get('page', 1)
    paginator = Paginator(pets, 8) # 5 pets per page
    try:
        pets = paginator.get_page(page)
    except PageNotAnInteger:
        pets = paginator.page(1)
    except EmptyPage:
        pets = paginator.page(1)
    context={'pets':pets}
    return render(request, 'doctors/doctor_browse_patients.html', context)

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
    for t in treatments:
        tr = t
    context={'treatments':treatments, 'pet': pet, 'tr':tr}
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

@login_required(login_url='login_doctor')
def dog_visits_history_list(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except:
        messages.error(request, 'dog is not exist')
        return redirect('doctor_browse_patients')
    visits = Visit.objects.filter(Q(pet = pet))
    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(visits, 2) # 5 per page
    try:
        visits = paginator.get_page(page)
    except PageNotAnInteger:
        visits = paginator.page(1)
    except EmptyPage:
        visits = paginator.page(1)
    context={'visits':visits, 'pet':pet}
    return render(request, 'doctors/visits_history.html', context)

@login_required(login_url='login_doctor')
def doctor_check_visits_list(request):
    visits = Visit.objects.filter(Q(doctor=request.user.profile.doctor) & Q(date__gte=date.today())).order_by('date')
    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(visits, 2) # 5 per page
    try:
        visits = paginator.get_page(page)
    except PageNotAnInteger:
        visits = paginator.page(1)
    except EmptyPage:
        visits = paginator.page(1)
    context={'visits':visits}
    return render(request, 'doctors/doctor_check_visits.html', context)

@login_required(login_url='login_doctor')
def add_medicines(request):
    form = MedicineCreationForm()
    if request.method == "POST":
        form = MedicineCreationForm(request.POST)
        if form.is_valid():
            medicine = form.save()
            messages.info(request, 'lek poprawnie dodano')
            return redirect('add_medicines')
        else:
            messages.error(request, 'nie można było dodać leku')
    context={'form':form}
    return render(request, "doctors/add_medicines.html", context)

@login_required(login_url='login_doctor')
def add_doctor_shift(request):
    form = DoctorShiftCreationForm
    if request.method == "POST":
        form = DoctorShiftCreationForm(request.POST)
        dates = request.POST.get()
        if form.is_valid():
            



            messages.info(request, 'poprawnie dodano dyżury')
            return redirect('home')# zmienić na jakąś stronkę co wyswietla wszystkie dyżury 
        else:
            messages.error(request, 'nie ustawiono dyżurów')
    context={'form':form}
    return render(request, "doctors/add_doctor_shift.html", context)