from datetime import date, datetime, timedelta, time
from django.contrib import messages
from django.contrib.auth import views as auth_views, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.db.models import Q	
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.urls import reverse

from backend.aaConfig.decorators import allowed_users, doctor_only
from backend.aaConfig.functions import pagination
from backend.doctors.models import Doctor, DoctorShift, Shift
from backend.pets.models import MedicineHistory, Pet, Medicine, Treatment
from backend.visits.models import Visit
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


######################### BROWSE PATIENS & CHECK VISITS ##############################

@login_required(login_url='login_doctor')
@doctor_only
def doctor_browse_patients(request):
    pets = Pet.objects.all()
    #paginations
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    pets = pets.filter(
        Q(name__icontains = q) | Q(owner__profile__name__icontains = q) | Q(race__icontains = q) | Q(year_birth__icontains = q)
    )
    pets = pagination(request,pets, 5)
    context={'pets':pets}
    return render(request, 'doctors/doctor_browse_patients.html', context)

@login_required(login_url='login_doctor')
@doctor_only
def doctor_check_visits_list(request):
    visits = Visit.objects.filter(Q(doctor=request.user.profile.doctor) & Q(date__gte=timezone.now()-timezone.timedelta(hours=5))).order_by('date')
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    visits = visits.filter(
        Q(date__icontains = q) |
        Q(pet__owner__profile__name__icontains = q) |
        Q(pet__name__icontains = q)
    ).order_by('date')
    #pagination
    visits = pagination(request, visits)
    text, text2, my_url = "Aktualne wizyty", "Sprawdź przeszłe wizyty", 'doctor_check_history_visits'
    context={'visits':visits, 'text':text, 'text2':text2, 'my_url':my_url}
    return render(request, 'doctors/doctor_check_visits.html', context)

@login_required(login_url='login_doctor')
@doctor_only
def doctor_remove_visit(request, visitid):
    try:
        visit = Visit.objects.get(id=visitid)
        visit.delete()
    except Visit.DoesNotExist:
        messages.error(request, 'wizyta nie istnieje')
    except:
        messages.error(request, 'nie można usunąć wyzyty')
    else:
        messages.info(request,'wizyta została usunięta')
    return redirect('doctor_check_visits')

@login_required(login_url='login_doctor')
@doctor_only
def doctor_check_history_visits_list(request):
    visits = Visit.objects.filter(Q(doctor=request.user.profile.doctor) & Q(date__lte=timezone.now())).order_by('-date')
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    visits = visits.filter(
        Q(date__icontains = q) |
        Q(pet__owner__profile__name__icontains = q) |
        Q(pet__name__icontains = q)
    ).order_by('-date')
    #pagination
    visits = pagination(request, visits)
    text, text2, my_url =  "Przeszłe wizyty","Sprawdź wizyty", 'doctor_check_visits'
    context={'visits':visits, 'text':text, 'text2':text2, 'my_url':my_url}
    return render(request, 'doctors/doctor_check_visits.html', context)


######################### PET HISTORY ##############################

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
    visits = Visit.objects.filter(Q(pet = pet) & Q(date__lte=timezone.now()))
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




######################### FUTURE VISITS ##############################

@login_required(login_url='login_doctor')
@doctor_only
def dog_future_visits_list(request, petid):
    try:
        pet = Pet.objects.get(id=petid)
    except:
        messages.error(request, 'pies nie istnieje')
        return redirect('doctor_browse_patients')
    visits = Visit.objects.filter(Q(pet = pet) & Q(date__gte=timezone.now())).order_by('date')
    context={'visits':visits, 'pet':pet}
    return render(request, 'doctors/future_visits_doctor.html', context)

@login_required(login_url='login_doctor')
@doctor_only
def remove_dog_future_visit(request,petid, visitid): 
    try:
        visit = Visit.objects.get(id=visitid)
        if visit.pet.id ==petid:
            visit.delete()
        else:
            messages.error(request, 'nie można usunąc wizyty innego pacjenta')
            return redirect('doctor_browse_patients')
    except Visit.DoesNotExist:
        messages.error(request, 'wizyta nie istnieje')
    except:
        messages.error(request, 'nie można usunąć wizyty')
    else:
        messages.info(request,'wizyta została usunięta')
    return redirect(reverse('dog_future_visits_list', kwargs={'petid':petid}))



######################### MEDICINES ##############################

@login_required(login_url='login_doctor')
@doctor_only
def medicine_list(request):
    medicines = Medicine.objects.all().order_by('name')
    #searching
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    medicines = medicines.filter(
        Q(name__icontains = q) |
        Q(description__icontains = q) |
        Q(producer__name__icontains = q)
    )
    #pagination
    medicines = pagination(request, medicines)
    context={'medicines':medicines}
    return render(request, "doctors/medicine_list.html", context)

@login_required(login_url='login_doctor')
@doctor_only
def remove_medicine(request, medicineid):
    try:
        medicine = Medicine.objects.get(id=medicineid)
        medicine.delete()
    except Medicine.DoesNotExist:
        messages.error(request, 'lek nie istnieje')
    except:
        messages.error(request, 'nie można usunąć leku')
    else:
        messages.info(request,'lek został usunięty')
    return redirect('medicine_list')

@login_required(login_url='login_doctor')
@doctor_only
def add_medicines(request):
    form = MedicineCreationForm()
    if request.method == "POST":
        form = MedicineCreationForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            for m in Medicine.objects.all():
                if m.name.lower() == medicine.name.lower() and m.producer.name == medicine.producer.name:
                    messages.error(request, 'lek już istnieje')
                    return redirect('add_medicines')
            medicine.save()
            messages.success(request, 'lek poprawnie dodano')
            return redirect('add_medicines')
        else:
            messages.error(request, 'nie można było dodać leku')
    context={'form':form}
    return render(request, "doctors/add_medicines.html", context)



######################### DOCTORSHIFTS ##############################

@login_required(login_url='login_doctor')
@doctor_only
def doctor_shift_list(request):
    doctorShifts = DoctorShift.objects.filter(Q(date__gte =datetime.today())).order_by('date','shift__startTime')
    doctorShifts = pagination(request, doctorShifts)
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




