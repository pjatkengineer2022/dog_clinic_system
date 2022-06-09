from datetime import datetime
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q	
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.utils import timezone

from backend.visits.models import Visit
from .models import Medicine, Pet, MedicineHistory
from .forms import PetCreateUpdateForm  #, PetAvatarCreateUpdateForm, PetCreateForm
from backend.aaConfig.functions import pagination
from backend.users.models import Owner


######################## DOG PROFILE ##########################

class PetListView(LoginRequiredMixin, ListView):
    model=Pet
    context_object_name = 'pets'
    paginate_by = 5
    template_name = 'pets/your_dogs.html'
    def get_queryset(self):
        try:
            user = self.request.user #User.objects.get(username=self.kwargs.get('username'))#self.kwargs.get('username') - pobiera z paska przeglądarki (z protokołu GET) atrybut 'username'
            owner = user.profile.owner  
            return Pet.objects.filter(owner=owner).order_by('name')     
        except:  
            messages.error(self.request, "nie można otworzyć strony twoich pupilów")
            return redirect('home')
    def get_context_data(self,**kwargs):
        context = super(PetListView, self).get_context_data(**kwargs)
        context['nearVisit'] = Visit.objects.filter(pet__owner=self.request.user.profile.owner).order_by('date').first()
        return context
       
@login_required
def edit_dog_profile(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except:
        messages.error(request, "nie można edytować psa")
        return redirect('your_dogs')
    if request.user.profile.owner == Owner.objects.filter(pet__id=id).first():
        profile_form=PetCreateUpdateForm(instance=pet)
        if request.method == 'POST':
            profile_form=PetCreateUpdateForm(request.POST, request.FILES, instance=pet)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, f'Profil dla {pet.name} został updatowany')
                return redirect(reverse('edit_dog', kwargs={'id':id})) 
            else:
                messages.error(request, f'Profil dla {pet.name} nie został updatowany')
        context={
            'pet':pet,
            'profile_form': profile_form,
        }
        return render(request, 'pets/edit_dog.html', context)
    else:
        messages.error(request, 'nie możesz edytować profilu nieswojego psa!')
        return redirect('your_dogs')

@login_required
def add_dog_profile(request):
    profile_form=PetCreateUpdateForm()
    if request.method == 'POST':
        profile_form=PetCreateUpdateForm(request.POST,request.FILES)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.owner = request.user.profile.owner
            profile.save()
            messages.success(request, f'Profil dla {profile.name} został utworzony')
            return redirect('your_dogs') 
        else:
            messages.error(request, 'Profil nie został utworzony')
    context={ 'profile_form': profile_form }
    return render(request, 'pets/add_dog.html', context)


###################### DOG HISTORY: DISEASES, MEDICINES, VISITS #########################

@login_required
def dog_diseases_list(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except:
        messages.error(request, 'pies nie istnieje')
        return redirect('your_dogs')
    if request.user.profile.owner == Owner.objects.filter(pet__id=id).first():
        #searching part:
        q= request.GET.get('q') if request.GET.get('q') != None else ''
        treatments = pet.treatment_set.all().filter(
            Q(disease__name__icontains = q)
            | Q(start__icontains = q)
            | Q(medicinehistory__medicine__name__icontains = q)
        )
        #pagination
        treatments = pagination(request, treatments)
        context={'treatments':treatments}
        return render(request, 'pets/disease.html', context)
    else:
        messages.error(request, 'nie możesz sprawdzić chorób dla nieswojego psa!')
        return redirect('your_dogs')

@login_required
def dog_medicines_list(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except:
        messages.error(request, 'pies nie istnieje')
        return redirect('your_dogs')
    if request.user.profile.owner == Owner.objects.filter(pet__id=id).first():
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
        context={'medicine_histories':medicine_histories}
        return render(request, 'pets/medicines.html', context)
    else:
        messages.error(request, 'nie możesz sprawdzić leków dla nieswojego psa!')
        return redirect('your_dogs')

@login_required
def dog_visits_list(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except:
        messages.error(request, 'pies nie istnieje')
        return redirect('your_dogs')
    if request.user.profile.owner == Owner.objects.filter(pet__id=id).first():
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
        context={'visits':visits,'pet':pet}
        return render(request, 'pets/visits.html', context)
    else:
        messages.error(request, 'nie możesz sprawdzić wizyt dla nieswojego psa!')
        return redirect('your_dogs')

######################### FUTURE VISITS ##############################
@login_required
def future_visits_list(request, petid):
    try:
        pet = Pet.objects.get(id=petid)
    except:
        messages.error(request, 'pies nie istnieje')
        return redirect('your_dogs')
    visits = Visit.objects.filter(Q(pet = pet) & Q(date__gte=timezone.now())).order_by('date')
    context={'visits':visits, 'pet':pet}
    return render(request, 'pets/future_visits.html', context)

@login_required
def remove_future_visit(request, petid, visitid): 
    try:
        pet = Pet.objects.get(id=petid)
    except:
        messages.error(request, 'pies nie istnieje')
        return redirect('your_dogs')
    if request.user.profile.owner == pet.owner:
        try:
            visit = Visit.objects.get(id=visitid)
            if visit.pet.id ==petid:
                visit.delete()
            else:
                messages.error(request, 'nie można usunąc wizyty innego z twoich psów')
                return redirect('your_dogs')
        except Visit.DoesNotExist:
            messages.error(request, 'wizyta nie istnieje')
        except:
            messages.error(request, 'nie można usunąć wizyty')
        else:
            messages.info(request,'wizyta została usunięta')
        return redirect(reverse('future_visits', kwargs={'petid':petid}))
    else:
        messages.error(request, 'nie można usunąc wizyty nieswojego psa')
        return redirect('your_dogs')
