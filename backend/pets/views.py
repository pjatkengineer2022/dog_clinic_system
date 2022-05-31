from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from visits.models import Visit

from .models import Medicine, Pet
from .forms import PetCreateUpdateForm  #, PetAvatarCreateUpdateForm, PetCreateForm

class PetListView(LoginRequiredMixin, ListView):
    model=Pet
    context_object_name = 'pets'
    paginate_by = 2
    template_name = 'pets/your_dogs.html'
    def get_queryset(self):
        try:
            user = self.request.user #User.objects.get(username=self.kwargs.get('username'))#self.kwargs.get('username') - pobiera z paska przeglądarki (z protokołu GET) atrybut 'username'
            owner = user.profile.owner  
            return Pet.objects.filter(owner=owner).order_by('name')     
        except:  
            messages.error(self.request, "nie można otworzyć strony twoich pupilów")
            return redirect('home')
       
@login_required
def edit_dog_profile(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except:
        messages.error(request, "nie można edytować twojego psa")
        return redirect('your_dogs')
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

@login_required
def dog_diseases_list(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except:
        messages.error(request, 'pies nie istnieje')
        return redirect('your_dogs')
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
    context={'treatments':treatments}
    return render(request, 'pets/disease.html', context)

@login_required
def dog_medicines_list(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except:
        messages.error(request, 'pies nie istnieje')
        return redirect('your_dogs')
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
    context={'treatments':treatments, 'medicines':medicines}
    return render(request, 'pets/medicines.html', context)

@login_required
def dog_visits_list(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except:
        messages.error(request, 'pies nie istnieje')
        return redirect('your_dogs')
    visits = Visit.objects.filter(pet = pet)
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
    return render(request, 'pets/visits.html', context)