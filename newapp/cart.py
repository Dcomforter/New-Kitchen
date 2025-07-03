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