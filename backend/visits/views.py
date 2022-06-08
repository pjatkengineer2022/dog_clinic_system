from django.shortcuts import redirect, render
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
from dateutil import parser, relativedelta
import pytz
from django.db.models import Q	
from django.utils import timezone

from .forms import DiagnosisCreationForm
from aaConfig.decorators import doctor_only
from .models import Diagnosis, Visit
from pets.models import Pet, Treatment, Medicine, MedicineHistory, Disease
from doctors.models import Doctor 
from users.models import Owner
# Create your views here.

@login_required(login_url='login_doctor')
@doctor_only
def add_diagnosis(request, visitid):
    try:
        visit = Visit.objects.get(id=visitid)
        pet=Pet.objects.get(id=visit.pet.id)
    except Visit.DoesNotExist:
        messages.error('nie można dodać diagnozy do wizyty która nie istnieje')
        return redirect('doctor_check_visit')
    except:
        messages.error('nie można dodać diagnozy do psa który nie istnieje')
        return redirect('doctor_check_visit')
    petTreatments = Treatment.objects.filter(pet=pet)
    allMedicines = Medicine.objects.all()
    form = DiagnosisCreationForm()
    if request.method == "POST":
        treatment_type = request.POST.get('treatment_type')
        new_disease_name = request.POST.get('new_disease')
        old_disease_treatment_id = request.POST.get('old_disease')
        petMedicines_id= request.POST.getlist('medicines') 
        form = DiagnosisCreationForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data.get('description')
            #Asign old treatment to diagnosis or create new treatment to diagnosis
            disease = None
            if treatment_type == '1' and new_disease_name != "":
                for d in Disease.objects.all():
                    if new_disease_name.lower().__eq__(d.name.lower()):
                        try:
                            disease = Disease.objects.get(id=d.id)
                        except Disease.DoesNotExist:
                            messages.error(request, 'nie można stworzyć diagnozy -choroba nie istnieje, (nieoczekiwany błąd)')
                            return redirect('doctor_check_visits')
                if disease is None:
                    try:
                        disease = Disease.objects.create(name=new_disease_name, description=" ")
                    except:
                        messages.error(request, 'nie udało się utworzyć nowej choroby (nieoczekiwany błąd)')
                        return redirect('doctor_check_visits')   
                try:
                    treatment = Treatment.objects.create(pet=pet, disease=disease)
                except:
                    messages.error(request, 'nie udało się utworzyć nowego leczenia (nieoczekiwany błąd)')
                    return redirect('doctor_check_visits')   
            elif treatment_type == '2' and old_disease_treatment_id != "":
                try:
                    treatment = Treatment.objects.get(id=old_disease_treatment_id)
                except Treatment.DoesNotExist:
                    messages.error(request, 'nie można stworzyć diagnozy -treatment(leczenie) nie istnieje, (nieoczekiwany błąd)')
                    return redirect('doctor_check_visits')
            else:
                messages.error(request, 'wpisz nową chorobę lub wybierz starą')
                context={'form':form, 'pet':pet, 'petTreatments':petTreatments, 'allMedicines':allMedicines}
                return render(request, 'visits/add_diagnosis.html', context)
            #create MedicineHistory --> assign medicines to treatment
            for medicine_id in petMedicines_id:
                try:
                    medicine = Medicine.objects.get(id=medicine_id)
                except Medicine.DoesNotExist:
                    messages.error(request, 'nie można stworzyć diagnozy - lek nie istnieje')
                    return redirect('doctor_check_visits')
                else:
                    MedicineHistory.objects.create(medicine=medicine, treatment=treatment)
            #create Diagnosis object
            try:
                Diagnosis.objects.create(visit= visit,treatment=treatment, description=description)
            except:
                messages.error(request,'nie można stworzyć diagnozy')
            else:
                messages.success(request,'poprawnie utworzono diagnozę')
                return redirect('doctor_check_visits')
        else:
            messages.error(request, 'musisz opisać objawy')
    context={'form':form, 'pet':pet, 'petTreatments':petTreatments, 'allMedicines':allMedicines}
    return render(request, 'visits/add_diagnosis.html', context)

@login_required(login_url='login_doctor')
@doctor_only
def add_diagnosis_no_visit(request, petid):
    try:
        pet=Pet.objects.get(id=petid)
    except Pet.DoesNotExist:
        messages.error('nie można dodać diagnozy do psa który nie istnieje')
        return redirect('doctor_check_visit')
    try:
        visit = Visit.objects.create(pet=pet, doctor = request.user.profile.doctor)
    except:
        messages.error('nie można utworzyćwizyty w celu utworzenia diagnozy')
        return redirect('doctor_check_visit')
    return redirect(reverse('add_diagnosis', kwargs={'visitid':visit.id}))


#function used in 4 below functions
def visitCreation(request, patients, doctors, renderSite, redirectSite, nearVisit=None):
    patients = patients
    doctors = doctors
    if request.method == "POST":
        #pet and doctor 
        try:
            patient = Pet.objects.get(id = request.POST.get('visitPatientId'))
            doctor = Doctor.objects.get(id = request.POST.get('visitDoctorId'))
        except Pet.DoesNotExist:
            messages.error(request, "Zwierzak lub Doktor nie istnieje")
            return redirect(redirectSite)
        #owner comment
        ownerComment = request.POST.get('visitOwnerComment')
        #convert date & check if already not exist:
        dateString = request.POST.get('visitDateISO')
        date = parser.parse(dateString)+relativedelta.relativedelta(hours=3)
        visitDateNotExisit = True
        for visit in Visit.objects.all():
            if visit.date == date and visit.doctor == doctor:
                visitDateNotExisit = False
        
        #error messages or creation 
        if visitDateNotExisit:
            if date >= pytz.UTC.localize(datetime.now()):
                if patient is not None and doctor is not None and ownerComment is not None and date is not None:
                    if patient in patients:    
                        if doctor in Doctor.objects.all():
                            if len(Visit.objects.filter(Q(pet=patient) & Q(date__gte=datetime.now()))) <3:
                                Visit.objects.create(pet=patient, doctor = doctor, ownerComment=ownerComment, date=date)
                                messages.success(request, 'Poprawnie zarezerwowałeś wizytę')
                                return redirect(redirectSite)    
                            else:
                                messages.error(request, 'nie można utworzyć więcej wizyt niż 3 dla jednego psa')
                        else:
                            messages.error(request, 'Doktor nie istnieje')
                    else:
                        messages.error(request, 'Pacjent nie istnieje')
                else:
                    messages.error(request, 'Nie podałeś wszystkich danych')
            else:
                messages.error(request, "Data nie może być wcześniejsza niż dzisiejszy dzień i aktualna godzina")
        else:
            messages.error(request, "Nie można dodać wizyty gdyż ten termin jest już zajęty")
    context={'patients':patients, 'doctors':doctors, 'nearVisit':nearVisit}
    return render(request, renderSite, context)


@login_required
def owner_book_visit_no_patient(request):
    patients = Pet.objects.filter(owner=request.user.profile.owner)
    doctors = Doctor.objects.all()
    nearVisit = Visit.objects.filter(Q(pet__owner=request.user.profile.owner) & Q(date__gt=timezone.now())).order_by('date').first()
    return visitCreation(request=request,patients=patients, doctors=doctors,  renderSite = 'visits/reservation.html', redirectSite='your_dogs', nearVisit=nearVisit)

@login_required(login_url='login_doctor')
@doctor_only
def doctor_book_visit_no_patient(request):
    patients = Pet.objects.all().order_by('name')
    doctor = request.user.profile.doctor
    return visitCreation(request=request,patients=patients, doctors=doctor, renderSite = 'visits/reservation_doctor.html', redirectSite='doctor_check_visits')

@login_required
def owner_book_visit_with_patient(request, petid):
    try:
        patients = [Pet.objects.get(id=petid)]
    except Pet.DoesNotExist:
        return redirect('your_dogs')
    if request.user.profile.owner == Owner.objects.filter(pet__id=petid).first():
        doctors = Doctor.objects.all()
        nearVisit = Visit.objects.filter(Q(pet__id=petid)  & Q(date__gt=timezone.now())).order_by('date').first()
        return visitCreation(request=request,patients=patients, doctors=doctors, renderSite = 'visits/reservation.html', redirectSite='your_dogs', nearVisit=nearVisit)
    else:
        messages.error(request, 'nie możesz zarezerwować wizyty dla nieswojego psa!')
        return redirect('your_dogs')


@login_required(login_url='login_doctor')
@doctor_only
def doctor_book_visit_with_patient(request, petid):
    try:
        patients = [Pet.objects.get(id=petid)]
    except Pet.DoesNotExist:
        return redirect('doctor_check_visits')
    doctor = request.user.profile.doctor
    nearVisit = Visit.objects.filter(Q(pet__id=petid)  & Q(date__gt=timezone.now())).order_by('date').first()
    return visitCreation(request=request,patients=patients, doctors=doctor,  renderSite = 'visits/reservation_doctor.html', redirectSite='doctor_check_visits', nearVisit=nearVisit)
    