from django.urls import path
from .views import PetListView, edit_dog_profile, add_dog_profile

urlpatterns = [
    path('your_dogs/', PetListView.as_view(), name='your_dogs'),
    path('edit_dog/<int:id>/', edit_dog_profile, name='edit_dog'),
    path('add_dog/', add_dog_profile, name='edit_dog'),
]
