from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from .models import Pet
from .forms import PetAvatarCreateUpdateForm, PetCreateUpdateForm

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
            #messages.error(self.request, "nie można otworzyć strony your_dogs.html")
            return redirect('home')
           
@login_required
def dog_profile_edit(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except:
        messages.error(request, "can't edit your dog")
        return redirect('home')#reverse('your_dogs', kwargs={'username':username}))
    profile_form=PetCreateUpdateForm(instance=pet)
    avatar_form= PetAvatarCreateUpdateForm(instance=pet)
    if request.method == 'POST':
        profile_form=PetCreateUpdateForm(request.POST, instance=pet)
        avatar_form=PetAvatarCreateUpdateForm(request.POST, request.FILES,  instance=pet)
        if profile_form.is_valid() and avatar_form.is_valid():
            profile_form.save()
            avatar_form.save()
            messages.success(request, f'Profile {pet.name} został updatowany')
            return redirect('') 
        else:
            messages.error(request, f'Profile {pet.name} nie został updatowany')
    context={
        'profile_form': profile_form,
        'avatar_form': avatar_form 
    }
    return render(request, 'pets/add_dog.html', context)

@login_required
def dog_profile_create(request):
    profile_form=PetCreateUpdateForm()
    avatar_form= PetAvatarCreateUpdateForm()
    if request.method == 'POST':
        profile_form=PetCreateUpdateForm(request.POST)
        avatar_form=PetAvatarCreateUpdateForm(request.POST, request.FILES)
        if profile_form.is_valid() and avatar_form.is_valid():
            profile_form.save()
            avatar_form.save()
            #messages.success(request, f'Profile {pet.name} został updatowany')
            return redirect('') 
        else:
            pass
            #messages.error(request, f'Profile {pet.name} nie został updatowany')
    context={
        'profile_form': profile_form,
        'avatar_form': avatar_form 
    }
    return render(request, 'pets/add_dog.html', context)
