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

def view_cart(request):
    cart = request.session.get('cart', {})

    # ✅ Clean up old malformed cart data
    for k, v in cart.items():
        if isinstance(v, int):
            cart[k] = {'quantity': v}
    request.session['cart'] = cart
    request.session.modified = True

    cart_instance = Cart(request)
    return render(request, 'cart.html', {'cart_items': cart_instance.items()})

def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id = str(item_id)

    # Ensure cart item is in the right format
    if item_id not in cart:
        cart[item_id] = {'quantity': 1}
    else:
        if isinstance(cart[item_id], dict):
            cart[item_id]['quantity'] += 1
        else:
            cart[item_id] = {'quantity': cart[item_id] + 1}

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('view_cart')

def remove_from_cart(request, item_id):
    cart = Cart(request)
    cart.remove(item_id)
    return redirect('view_cart')

def checkout(request):
    cart = Cart(request)
    print("🧺 CART CONTENT @checkout:", cart)
    cart_items = cart.items()
    total = sum(item['subtotal'] for item in cart_items)
    
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total
    })

def submit_order(request):
    print("🛎️ submit_order view was called")  # Should always print
    cart = request.session.get('cart', {})
    if not cart:
        print("⚠️ Cart is empty at submit_order.")
        return redirect('view_cart')

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        order_notes = request.POST.get('order_notes', '')

        for item_id, item in cart.items():
            menu_item = get_object_or_404(Menu, id=int(item_id))  # ✅ Cast item_id to int
            Order.objects.create(
                menu_item=menu_item,
                customer_name=customer_name,
                customer_email=customer_email,
                quantity=item['quantity'],
                order_notes=order_notes,
                fulfilled=False,
            )

        # ✅ Clear cart after order
        if 'cart' in request.session:
            del request.session['cart']
            request.session.modified = True
            print("✅ Cart cleared successfully")
        else:
            print("⚠️ Cart key not found in session")

        return render(request, 'order_success.html', {
            'customer_name': customer_name
        })

    return redirect('checkout')

