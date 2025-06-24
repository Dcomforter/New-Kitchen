from django.contrib import admin
from newapp.models import Booking, Menu, Order

class MenuAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'cuisine', 'price')
    fields = ('food_name', 'cuisine', 'item_description', 'price', 'image')  # Include image here

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'menu_item', 'quantity', 'fulfilled', 'created_at']
    list_filter = ['fulfilled', 'created_at']
    search_fields = ['customer_name', 'customer_email']


# Register your models here.
admin.site.register(Booking)
admin.site.register(Menu)
