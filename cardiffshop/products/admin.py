from products.models import Product, Category, ProductImage
from django.contrib import admin
from django.contrib.admin import SimpleListFilter


class CanBeSoldListFilter(SimpleListFilter):
    title = "Can be sold"
    parameter_name = "can_be_sold"

    def lookups(self, request, model_admin):
        return (
            ("1", "Yes"),
            ("0", "No")
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == "1":
            return queryset.filter(stock_count__gt=0)
        if value == "0":
            return queryset.filter(stock_count=0)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "stock_count", "can_be_sold")
    list_filter = ("category", "date_created", CanBeSoldListFilter)
    search_fields = ("name", "description", "sku_number", "barcode")

    readonly_fields = ("date_created", )
    prepopulated_fields = {"slug": ("name",)}
    radio_fields = {"campaign": admin.VERTICAL}

    fieldsets = (
        (None, {
            "fields": ("category", "name", "slug", "description"),
            "classes": ("suit-tab", "suit-tab-identity",),
        }),
        (None, {
            "fields": (("price", "price_unit"), "campaign", "campaign_end_date", "damaged"),
            "classes": ("suit-tab", "suit-tab-price",),
        }),
        (None, {
            "fields": ("barcode", "sku_number", "stock_count", "is_visible", "date_created"),
            "classes": ("suit-tab", "suit-tab-stock",),
        }),
    )

    suit_form_tabs = (
        ('identity', 'Identity'),
        ('price', 'Price'),
        ('stock', 'Stock')
    )

    def can_be_sold(self, obj):
        """
        Determines whether the product can be sold or not.
        """
        if obj.stock_count > 0:
            return True
        else:
            return False

    can_be_sold.boolean = True

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
