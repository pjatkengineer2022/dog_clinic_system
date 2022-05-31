from datetime import date, datetime, timedelta
from django.contrib import messages
from django.contrib.auth import views as auth_views, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q	
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from aaConfig.decorators import allowed_users, doctor_only
from doctors.models import Doctor, DoctorShift, Shift
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
        return redirect('doctor_check_visits')

# class DoctorBrowsePatientListView(LoginRequiredMixin, ListView):
#     model=Pet
#     template_name = 'doctors/doctor_browse_patients.html'
#     context_object_name = 'pets'
#     paginate_by = 2
#     login_url = 'login_doctor'
@login_required(login_url='login_doctor')
@doctor_only
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
@doctor_only
def dog_diseases_history_list(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except:
        messages.error(request, 'pies nie istnieje')
        return redirect('doctor_browse_patients')
    #searching part:
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    treatments = pet.treatment_set.all().filter(
        Q(disease__name__icontains = q)
        | Q(start__icontains = q)
        | Q(medicinehistory__medicine__name__icontains = q)
    )
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
@doctor_only
def dog_medicines_history_list(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except:
        messages.error(request, 'pies nie istnieje')
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
@doctor_only
def dog_visits_history_list(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except:
        messages.error(request, 'pies nie istnieje')
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
@doctor_only
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
@doctor_only
def add_medicines(request):
    form = MedicineCreationForm()
    if request.method == "POST":
        form = MedicineCreationForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            for m in Medicine.objects.all():
                if m.name.lower() == medicine.name.lower():
                    messages.error(request, 'lek już istnieje')
                    return redirect('add_medicines')
            medicine.save()
            messages.success(request, 'lek poprawnie dodano')
            return redirect('add_medicines')
        else:
            messages.error(request, 'nie można było dodać leku')
    context={'form':form}
    return render(request, "doctors/add_medicines.html", context)

@login_required(login_url='login_doctor')
@doctor_only
def add_doctor_shift(request):
    form = DoctorShiftCreationForm
    if request.method == "POST":
        form = DoctorShiftCreationForm(request.POST)
        datepicker = request.POST.get('datepicker')
        if datepicker is not None:
            dates = [datetime.strptime(strD, '%Y-%m-%d') for strD in datepicker.split(',')]
            if form.is_valid():
                doctor = request.user.profile.doctor
                shift = form.cleaned_data['shift']
                for date in dates:
                    print(doctor, shift, date)
                    #check if date is before today
                    if date.date() < datetime.today().date():
                        messages.error(request, 'nie można dodać wcześniejszej daty niż dzisiejsza')
                        context = {'form':form}
                        return render(request, "doctors/add_doctor_shift.html", context)
                    #check if doctorshift exist
                    for dsft in DoctorShift.objects.all():
                        if dsft.date == date.date() and dsft.shift.name == shift.name and dsft.shift.startTime == shift.startTime and dsft.shift.endTime == shift.endTime:
                            messages.error(request, f'Dyżur {shift.name}, dnia {date.strftime("%Y-%m-%d")} już istnieje!')
                            context = {'form':form}
                            return render(request, "doctors/add_doctor_shift.html", context)
                    #create and save new DoctorShift
                    try:
                        DoctorShift.objects.create(shift=shift ,doctor=doctor, date=date)
                    except:
                        messages.error(request, f'nie można dodać dyżurów')
                        context = {'form':form}
                        return render(request, "doctors/add_doctor_shift.html", context)
                messages.success(request, 'poprawnie dodano dyżury')
                return redirect('doctor_shift_list')# zmienić na jakąś stronkę co wyswietla wszystkie dyżury 
            else:
                messages.error(request, 'nie ustawiono dyżurów')
        else:
            messages.error(request, 'musisz wybrać chociaż jedną datę')
    context={'form':form}
    return render(request, "doctors/add_doctor_shift.html", context)

@login_required(login_url='login_doctor')
@doctor_only
def remove_doctor_shift(request, id): 
    try:
        dsft = DoctorShift.objects.get(id=id)
        dsft.delete()
    except DoctorShift.DoesNotExist:
        messages.error(request, 'dyżur nie istnieje')
    except:
        messages.error(request, 'nie można usunąć dyżuru')
    else:
        messages.info(request,'dyżur został usunięty')
    return redirect('doctor_shift_list')

@login_required(login_url='login_doctor')
@doctor_only
def doctor_shift_list(request):
    doctorShifts = DoctorShift.objects.filter(date__gte =datetime.today()).order_by('date','shift__startTime')
    context={'doctorShifts':doctorShifts}
    return render(request, "doctors/doctor_shift_list.html", context)

