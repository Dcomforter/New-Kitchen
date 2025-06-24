from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from newapp.forms import BookingForm, OrderForm
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

def menu_details(request, item_id):
    menu_item = get_object_or_404(Menu, id=item_id)
    order_success = False

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.menu_item = menu_item
            order.save()
            order_success = True
    else:
        form = OrderForm()

    return render(request, 'menu_details.html', {
        'menu_item': menu_item,
        'form': form,
        'order_success': order_success
    })


# def menu_details(request, pk=None):
#     if pk:
#         menu_item = Menu.objects.get(pk=pk)
#     else:
#         menu_item = ''
    
#     return render(request, 'menu_details.html', {"menu_item" : menu_item})

# def menu_details(request, id):
#     menu = Menu.objects.get(id=id)
#     template = loader.get_template('menu_details.html')
#     context = {'menu_item' : menu}

#     return HttpResponse(template.render(context, request))

def place_order(request, item_id):
    menu_item = get_object_or_404(Menu, id=item_id)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.menu_item = menu_item
            order.save()
            return redirect('order_success')
    else:
        form = OrderForm()
    return render(request, 'order_page.html', {'form': form})

def order_success(request):
    return render(request, 'order_success.html')