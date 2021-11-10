from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInLine(admin.TabularInline):
    """
    InLine Admin configuration for OrderLineItem model
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Order model
    """
    inlines = (OrderLineItemAdminInLine,)

    readonly_fields = ('order_number', 'date', 'delivery_cost',
                       'previous_total', 'discount',
                       'order_total', 'grand_total',
                       'original_basket', 'stripe_pid')

    fields = ('order_number', 'user_profile',
              'date', 'full_name', 'email',
              'phone_number', 'address_1',
              'address_2', 'town_or_city', 'county',
              'postcode', 'country',
              'previous_total',
              'discount', 'order_total',
              'delivery_cost', 'grand_total',
              'original_basket', 'stripe_pid')

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total')

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
