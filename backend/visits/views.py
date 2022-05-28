from django.shortcuts import redirect, render
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import DiagnosisCreationForm
from aaConfig.decorators import doctor_only
from .models import Diagnosis, Visit
from pets.models import Pet, Treatment, Medicine, MedicineHistory, Disease
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
            if len(petMedicines_id) != 0:
                #Asign old treatment to diagnosis or create new treatment to diagnosis
                disease = None
                if treatment_type == '1' and new_disease_name != "":
                    for d in Disease.objects.all():
                        if new_disease_name.lower() == d.name.lower():
                            try:
                                disease = Disease.objects.get(id=d.id)
                            except Disease.DoesNotExist:
                                messages('nie można stworzyć diagnozy -choroba nie istnieje, (nieoczekiwany błąd)')
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
                        messages('nie można stworzyć diagnozy -treatment(leczenie) nie istnieje, (nieoczekiwany błąd)')
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
                        messages(request, 'nie można stworzyć diagnozy - lek nie istnieje')
                        return redirect('doctor_check_visits')
                    else:
                        MedicineHistory.objects.create(medicine=medicine, treatment=treatment)
                #create Diagnosis object
                try:
                    Diagnosis.objects.create(visit= visit,treatment=treatment, description=description)
                except:
                    messages.error(request,'nie można stworzyć diagnozy')
                else:
                    messages.info(request,'poprawnie utworzono diagnozę')
                    return redirect('doctor_check_visits')
            else:
                messages.error(request, 'musisz wybrać leki')
        else:
            messages.error(request, 'musisz opisać objawy')
    context={'form':form, 'pet':pet, 'petTreatments':petTreatments, 'allMedicines':allMedicines}
    return render(request, 'visits/add_diagnosis.html', context)

