from django.contrib import admin
from newapp.models import Booking, Menu

class MenuAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'cuisine', 'price')
    fields = ('food_name', 'cuisine', 'item_description', 'price', 'image')  # Include image here


# Register your models here.
admin.site.register(Booking)
admin.site.register(Menu)
