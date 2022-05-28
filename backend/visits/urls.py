from django.urls import path
from . import views
urlpatterns = [
    path('add_diagnosis/<int:visitid>/',views.add_diagnosis, name='add_diagnosis'),
]