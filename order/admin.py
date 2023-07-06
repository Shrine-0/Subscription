from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ['price', 'user', 'created_at','payment_status','payment_mode']
    
# admin.site.register(Order)