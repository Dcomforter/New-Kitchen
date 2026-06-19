from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .cart import Cart
from .models import Menu, Order
from .serializers import CartSerializer, MenuSerializer, OrderSerializer


class MenuListAPIView(generics.ListAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        queryset = Menu.objects.order_by('id')
        featured = self.request.query_params.get('featured')
        if featured is not None:
            queryset = queryset.filter(is_featured=featured.lower() in ('1', 'true', 'yes'))
        return queryset


class MenuDetailAPIView(generics.RetrieveAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


def _cart_payload(request):
    cart = Cart(request)
    cart_items = cart.items()
    grand_total = sum(item['subtotal'] for item in cart_items)
    return {'items': cart_items, 'grand_total': grand_total}


class CartDetailAPIView(APIView):
    def get(self, request):
        serializer = CartSerializer(_cart_payload(request))
        return Response(serializer.data)


class CartAddAPIView(APIView):
    def post(self, request, item_id):
        get_object_or_404(Menu, id=item_id)
        quantity = max(int(request.data.get('quantity', 1)), 1)
        order_notes = request.data.get('order_notes', '').strip()

        cart = Cart(request)
        cart.add(item_id, quantity=quantity, order_notes=order_notes)

        serializer = CartSerializer(_cart_payload(request))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemAPIView(APIView):
    def patch(self, request, item_id):
        cart = Cart(request)
        item_id = str(item_id)

        if item_id not in cart.cart:
            return Response({'error': 'Item not in cart'}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')
        if action == 'increase':
            cart.cart[item_id]['quantity'] += 1
        elif action == 'decrease':
            cart.cart[item_id]['quantity'] = max(1, cart.cart[item_id]['quantity'] - 1)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        cart.save()

        menu_item = get_object_or_404(Menu, id=item_id)
        quantity = cart.cart[item_id]['quantity']
        subtotal = quantity * menu_item.price

        return Response({'quantity': quantity, 'subtotal': f'{subtotal:.2f}'})

    def delete(self, request, item_id):
        cart = Cart(request)
        cart.remove(item_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartCheckoutAPIView(APIView):
    def post(self, request):
        cart = Cart(request)
        cart_items = cart.items()

        if not cart_items:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        customer_name = request.data.get('customer_name')
        customer_email = request.data.get('customer_email')
        notes = request.data.get('notes', {})

        orders = []
        for item in cart_items:
            item_id = str(item['menu_item'].id)
            orders.append(Order.objects.create(
                menu_item=item['menu_item'],
                customer_name=customer_name,
                customer_email=customer_email,
                quantity=item['quantity'],
                order_notes=notes.get(item_id, item['notes']),
                fulfilled=False,
            ))

        cart.clear()

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MenuOrderAPIView(APIView):
    def post(self, request, item_id):
        menu_item = get_object_or_404(Menu, id=item_id)

        serializer = OrderSerializer(data={
            'menu_item': menu_item.id,
            'customer_name': request.data.get('customer_name'),
            'customer_email': request.data.get('customer_email'),
            'quantity': request.data.get('quantity', 1),
            'order_notes': request.data.get('order_notes', ''),
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
