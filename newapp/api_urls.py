from django.urls import path
from . import api_views

urlpatterns = [
    path('menu/', api_views.MenuListAPIView.as_view(), name='api_menu_list'),
    path('menu/<int:pk>/', api_views.MenuDetailAPIView.as_view(), name='api_menu_detail'),
    path('menu/<int:item_id>/order/', api_views.MenuOrderAPIView.as_view(), name='api_menu_order'),
    path('cart/', api_views.CartDetailAPIView.as_view(), name='api_cart_detail'),
    path('cart/add/<int:item_id>/', api_views.CartAddAPIView.as_view(), name='api_cart_add'),
    path('cart/items/<int:item_id>/', api_views.CartItemAPIView.as_view(), name='api_cart_item'),
    path('cart/checkout/', api_views.CartCheckoutAPIView.as_view(), name='api_cart_checkout'),
]
