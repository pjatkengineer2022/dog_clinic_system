from django.shortcuts import redirect, render
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import DiagnosisCreationForm
from aaConfig.decorators import doctor_only
from .models import Diagnosis, Visit
from pets.models import Pet, Treatment, Medicine, MedicineHistory, Disease
from doctors.models import Doctor 
from datetime import datetime
from dateutil import parser, relativedelta
import pytz
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
                    if new_disease_name.lower() == d.name.lower():
                        try:
                            disease = Disease.objects.get(id=d.id)
                        except Disease.DoesNotExist:
                            messages.error(request, 'nie można stworzyć diagnozy -choroba nie istnieje, (nieoczekiwany błąd)')
                            return redirect('doctor_check_visits')
                if disease is not None:
                    disease = Disease.objects.create(name=new_disease_name, description=" ")
                else:
                    messages.error(request, 'nie wpisano nowej choroby (nieoczekiwany błąd)')
                    return redirect('doctor_check_visits')   
                treatment = Treatment.objects.create(pet=pet, disease=disease)
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

#function used in 4 below functions
def visitCreation(request, patients, doctors, renderSite, redirectSite):
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
                        if doctor in doctors:
                            Visit.objects.create(pet=patient, doctor = doctor, ownerComment=ownerComment, date=date)
                            messages.success(request, 'Poprawnie zarezerwowałeś wizytę')
                            return redirect(redirectSite)
                        else:
                            messages.error(request, 'Doktor nie istnieje')
                    else:
                        messages.error(request, 'Pacjent nie istnieje')
                else:
                    messages.error(request, 'Nie podałeś wszystkich danych')
            else:
                messages.error(request, "Data nie może być wcześniejsza niż dzisiaj")
        else:
            messages.error(request, "Nie można dodać wizyty gdyż ten termin jest już zajęty")
    context={'patients':patients, 'doctors':doctors}
    return render(request, renderSite, context)


@login_required
def owner_book_visit_no_patient(request):
    patients = Pet.objects.filter(owner=request.user.profile.owner)
    doctors = Doctor.objects.all()
    return visitCreation(request=request,patients=patients, doctors=doctors,  renderSite = 'visits/reservation.html', redirectSite='your_dogs')

@login_required(login_url='login_doctor')
@doctor_only
def doctor_book_visit_no_patient(request):
    patients = Pet.objects.all()
    doctors = request.user.profile.doctor
    return visitCreation(request=request,patients=patients, doctors=doctors, renderSite = 'visits/reservation_doctor.html', redirectSite='doctor_check_visits')

@login_required
def owner_book_visit_with_patient(request, petid):
    try:
        patients = Pet.objects.get(id=petid)
    except Pet.DoesNotExist:
        return redirect('your_dogs')
    doctors = Doctor.objects.all()
    return visitCreation(request=request,patients=patients, doctors=doctors, renderSite = 'visits/reservation.html', redirectSite='your_dogs')
    
@login_required(login_url='login_doctor')
@doctor_only
def doctor_book_visit_with_patient(request, petid):
    try:
        patients = Pet.objects.get(id=petid)
    except Pet.DoesNotExist:
        return redirect('doctor_check_visits')
    doctors = request.user.profile.doctor
    return visitCreation(request=request,patients=patients, doctors=doctors,  renderSite = 'visits/reservation_doctor.html', redirectSite='doctor_check_visits')
    