from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from newapp.models import Booking, Menu, Order

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['food_name', 'cuisine', 'price', 'is_featured']
    list_editable = ['is_featured']  # toggle directly from the list view
    list_filter = ['is_featured', 'cuisine']
    list_per_page = 10

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'menu_item', 'quantity', 'fulfilled', 'created_at']
    list_filter = ['fulfilled', 'created_at']
    search_fields = ['customer_name', 'customer_email']
    readonly_fields = ('subtotal',)
    list_per_page = 10
    actions = ['print_ticket']

    def print_ticket(self, request, queryset):
        ids = ','.join(str(pk) for pk in queryset.values_list('id', flat=True))
        url = reverse('print_tickets')
        return HttpResponseRedirect(f"{url}?ids={ids}")
    print_ticket.short_description = "Print kitchen ticket(s)"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_per_page = 10

# Register your models here.
# admin.site.register(Menu)
