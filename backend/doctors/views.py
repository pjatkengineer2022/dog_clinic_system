from datetime import date, datetime, timedelta
from django.contrib import messages
from django.contrib.auth import views as auth_views, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.db.models import Q	
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from aaConfig.decorators import allowed_users, doctor_only
from aaConfig.functions import pagination
from doctors.models import Doctor, DoctorShift, Shift
from pets.models import MedicineHistory, Pet, Medicine, Treatment
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
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    pets = pets.filter(
        Q(name__icontains = q) | Q(owner__profile__name__icontains = q) | Q(race__icontains = q) | Q(year_birth__icontains = q)
    )
    pets = pagination(request,pets)
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
    treatments = pagination(request, treatments)
    context={'treatments':treatments, 'pet': pet}
    return render(request, 'doctors/disease_history.html', context)

@login_required(login_url='login_doctor')
@doctor_only
def dog_medicines_history_list(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except:
        messages.error(request, 'pies nie istnieje')
        return redirect('doctor_browse_patients')
    #treatments = pet.treatment_set.all()
    #searching part
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    treatments = pet.treatment_set.all().filter(
        Q(medicinehistory__medicine__name__icontains = q)
        | Q(medicinehistory__medicine__producer__name__icontains = q)
        | Q(start__icontains = q)
        | Q(disease__name__icontains = q)
    )
    medicine_histories = MedicineHistory.objects.filter(treatment__in=treatments)
    #pagination
    medicine_histories = pagination(request, medicine_histories)
    context={'pet':pet, 'medicine_histories':medicine_histories}
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
    #searching part
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    visits = visits.filter(
        Q(doctor__profile__name__icontains = q) |
        Q(date__icontains = q) |
        Q(diagnosis__treatment__disease__name__icontains = q)
    )
    #pagination
    visits = pagination(request, visits)
    context={'visits':visits, 'pet':pet}
    return render(request, 'doctors/visits_history.html', context)

@login_required(login_url='login_doctor')
@doctor_only
def doctor_check_visits_list(request):
    visits = Visit.objects.filter(Q(doctor=request.user.profile.doctor) & Q(date__gte=date.today())).order_by('date')
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    visits = visits.filter(
        Q(date__icontains = q) |
        Q(pet__owner__profile__name__icontains = q) |
        Q(pet__name__icontains = q)
    ).order_by('date')
    #pagination
    visits = pagination(request, visits)
    context={'visits':visits}
    return render(request, 'doctors/doctor_check_visits.html', context)


@login_required(login_url='login_doctor')
@doctor_only
def doctor_shift_list(request):
    doctorShifts = DoctorShift.objects.filter(date__gte =datetime.today()).order_by('date','shift__startTime')
    doctorShifts = pagination(request, doctorShifts, 10)
    context={'doctorShifts':doctorShifts}
    return render(request, "doctors/doctor_shift_list.html", context)

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

