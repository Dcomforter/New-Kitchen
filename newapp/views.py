from django.shortcuts import render
from django.http import HttpResponse
from newapp.forms import BookingForm
from newapp.models import Menu
from django.template import loader

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

# This view shows the reservation form for booking
def form_view(request):
    reservation_successful = False
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            reservation_successful = True
    else:
        form = BookingForm()

    context = {"form" : form, "reservation_successful" : reservation_successful}
    return render(request, "reservation.html", context)

def kitchen(request):
    menu = Menu.objects.all().values()
    template = loader.get_template('kitchen.html')
    context = {'menu' : menu}

    return HttpResponse(template.render(context, request))

def menu_details(request, pk=None):
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ''
    
    return render(request, 'menu_details.html', {"menu_item" : menu_item})

# def menu_details(request, id):
#     menu = Menu.objects.get(id=id)
#     template = loader.get_template('menu_details.html')
#     context = {'menu_item' : menu}

#     return HttpResponse(template.render(context, request))