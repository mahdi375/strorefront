from django.db.models.aggregates import Count
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from . import models
from tag.models import TaggedItem


class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']
    extra = 1


@admin.register(models.Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['description', 'discount']


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        return collection.products_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    list_display = [
        'id',
        'title',
        'collection',
        'unit_price',
        'inventory_status'
    ]
    ordering = ['-id']
    list_per_page = 10
    list_editable = ['unit_price']
    list_select_related = ['collection']
    list_filter = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }

    @admin.display(ordering='inventory')
    def inventory_status(self, product: models.Product):
        return 'OK' if product.inventory >= 10 else 'LOW'
