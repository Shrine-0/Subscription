from django.contrib import admin

from . models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ['price', 'user', 'createdAt']


# admin.site.register(Product,ProductAdmin)