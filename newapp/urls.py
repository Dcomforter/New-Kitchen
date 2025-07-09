from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('kitchen/', views.kitchen, name='kitchen'),
    path('reservation/', views.form_view, name='reservation' ),
    path('menu_details/<int:item_id>/', views.menu_details, name='menu_details'),
    path('kitchen/menu_details/<int:item_id>/', views.menu_details, name='menu_details'),
    path('place_order/<int:item_id>/', views.place_order, name='place_order'), 
    path('order_success/', views.order_success, name='order_success'),
    path('about/', views.about, name="about"),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update_quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('submit_order/', views.submit_order, name='submit_order'),       
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)