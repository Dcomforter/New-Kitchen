from rest_framework import serializers
from .models import Menu, Order


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            'id', 'food_name', 'cuisine', 'item_description',
            'price', 'prep_time', 'calories', 'image', 'is_featured',
        ]


class OrderSerializer(serializers.ModelSerializer):
    menu_item_detail = MenuSerializer(source='menu_item', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'menu_item', 'menu_item_detail', 'customer_name', 'customer_email',
            'quantity', 'order_notes', 'created_at', 'fulfilled', 'subtotal',
        ]
        read_only_fields = ['created_at', 'fulfilled']


class CartItemSerializer(serializers.Serializer):
    menu_item = MenuSerializer()
    quantity = serializers.IntegerField()
    notes = serializers.CharField(allow_blank=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)


class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    grand_total = serializers.DecimalField(max_digits=10, decimal_places=2)
