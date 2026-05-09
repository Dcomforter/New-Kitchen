from django.contrib import admin
from newapp.models import Booking, Menu, Order

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['food_name', 'cuisine', 'price', 'is_featured']
    list_editable = ['is_featured']  # toggle directly from the list view
    list_filter = ['is_featured', 'cuisine']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'menu_item', 'quantity', 'fulfilled', 'created_at']
    list_filter = ['fulfilled', 'created_at']
    search_fields = ['customer_name', 'customer_email']
    readonly_fields = ('subtotal',)
    

# Register your models here.
admin.site.register(Booking)
admin.site.register(Menu)
