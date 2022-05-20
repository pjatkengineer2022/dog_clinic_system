from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from .models import Pet
from .forms import PetCreateUpdateForm  #, PetAvatarCreateUpdateForm, PetCreateForm

class PetListView(LoginRequiredMixin, ListView):
    model=Pet
    context_object_name = 'pets'
    paginate_by = 5
    template_name = 'pets/your_dogs2.html'
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
        messages.error(request, "can't edit your dog")
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

