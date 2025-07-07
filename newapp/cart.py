from .models import Menu

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, menu_item_id, quantity=1):
        menu_item_id = str(menu_item_id)
        if menu_item_id in self.cart:
            self.cart[menu_item_id] += quantity
        else:
            self.cart[menu_item_id] = quantity
        self.save()

    def remove(self, menu_item_id):
        menu_item_id = str(menu_item_id)
        if menu_item_id in self.cart:
            del self.cart[menu_item_id]
            self.save()    

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True

    def items(self):
        cart_items = []
        for item_id, item_data in self.cart.items():
            try:
                menu_item = Menu.objects.get(pk=item_id)
                quantity = item_data['quantity'] if isinstance(item_data, dict) else item_data
                cart_items.append({
                    'menu_item': menu_item,
                    'quantity': quantity,
                    'total_price': quantity * menu_item.price
                })
            except Menu.DoesNotExist:
                continue
        return cart_items
