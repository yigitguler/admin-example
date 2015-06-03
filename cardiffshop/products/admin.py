from products.models import Product, Category, ProductImage
from django.contrib import admin


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category", "date_created")
    search_fields = ("name", "description", "sku_number", "barcode_number")


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
