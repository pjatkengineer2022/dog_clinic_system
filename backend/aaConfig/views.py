from django.shortcuts import render


def home(request):
    context={}
    return render(request, 'home.html', context)
def contact(request):
    context={}
    return render(request, 'contact.html', context)

def page_404_not_found(request, exception):
    return render(request, "http404.html")