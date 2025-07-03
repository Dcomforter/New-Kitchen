from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from newapp.forms import BookingForm, OrderForm
from newapp.models import Menu, Order
from django.template import loader
from .cart import Cart
from django.contrib import messages

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

def cart_view(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart_items': cart.items()})

def add_to_cart(request, item_id):
    cart = Cart(request)
    cart.add(item_id)
    return redirect('cart_view')

def remove_from_cart(request, item_id):
    cart = Cart(request)
    cart.remove(item_id)
    return redirect('cart_view')

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.info(request, "Your cart is empty.")
        return redirect('kitchen')

    items = []
    total_price = 0
    for item_id, item_data in cart.items():
        try:
            menu_item = Menu.objects.get(pk=item_id)
            quantity = item_data['quantity']
            items.append({
                'menu_item': menu_item,
                'quantity': quantity,
                'subtotal': menu_item.price * quantity,
            })
            total_price += menu_item.price * quantity
        except Menu.DoesNotExist:
            continue

    return render(request, 'checkout.html', {
        'items': items,
        'total_price': total_price,
    })

def submit_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        name = request.POST.get('name')
        email = request.POST.get('email')
        notes = request.POST.get('notes', '')

        if not name or not email:
            messages.error(request, "Name and Email are required.")
            return redirect('checkout')

        for item_id, item_data in cart.items():
            try:
                menu_item = Menu.objects.get(pk=item_id)
                quantity = item_data['quantity']
                Order.objects.create(
                    menu_item=menu_item,
                    customer_name=name,
                    customer_email=email,
                    quantity=quantity,
                    order_notes=notes,
                    fulfilled=False
                )
            except Menu.DoesNotExist:
                continue

        # Clear the cart
        request.session['cart'] = {}
        messages.success(request, "Your order has been placed successfully!")
        return redirect('menu')

    return redirect('checkout')