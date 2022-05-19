from django.urls import path
from .views import PetListView, dog_profile_edit

urlpatterns = [
    path('your_dogs/', PetListView.as_view(), name='your_dogs'),
    path('edit_dog/<int:id>', dog_profile_edit, name='edit_dog'),
    #path('add_dog/', , name='add_dog'),
]
