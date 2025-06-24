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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)