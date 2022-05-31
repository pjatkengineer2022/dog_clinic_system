from django.shortcuts import render
from doctors.models import Service

def home(request):
    context={}
    return render(request, 'home.html', context)
def contact(request):
    context={}
    return render(request, 'contact.html', context)
def prices(request):
    services = Service.objects.all()
    context = {'services':services}
    return render(request, 'price_list.html', context)



def page_404_not_found(request, exception):
    return render(request, "http404.html")