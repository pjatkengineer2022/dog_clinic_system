from django.urls import path
from .views import PetListView, edit_dog_profile, add_dog_profile, dog_diseases_list, dog_medicines_list, dog_visits_list, future_visits_list, remove_future_visit

urlpatterns = [
    path('your_dogs/', PetListView.as_view(), name='your_dogs'),
    path('edit_dog/<int:id>/', edit_dog_profile, name='edit_dog'),
    path('add_dog/', add_dog_profile, name='add_dog'),
    path('diseases/<int:id>/', dog_diseases_list, name='dog_diseases'),
    path('medicines/<int:id>/', dog_medicines_list, name='dog_medicines'),
    path('visits/<int:id>/', dog_visits_list, name='dog_visits'),
    # FUTURE VISITS:
    path('future_visits/<int:petid>/', future_visits_list, name='future_visits'),
    path('remove_future_visit/<int:petid>/<int:visitid>/', remove_future_visit, name='remove_future_visit'),

]