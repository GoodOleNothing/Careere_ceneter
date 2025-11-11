from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import NetworkNode, Product


@admin.action(description='Обнулить задолженность перед поставщиком для выбранных')
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=0)


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    readonly_fields = ()


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'supplier_link', 'country', 'city', 'debt', 'created_at')
    list_filter = ('city', 'country', 'level')
    search_fields = ('name', 'city', 'country', 'street')
    actions = [clear_debt]
    inlines = [ProductInline]
    readonly_fields = ('created_at', 'level', 'supplier_link_readonly')
    fieldsets = (
        (None, {
            'fields': (
                'name', 'supplier', 'supplier_link_readonly',
                ('email', 'country', 'city'),
                ('street', 'house_number'),
                'debt',
                'level',
                'created_at'
            )
        }),
    )

    def supplier_link(self, obj):
        if obj.supplier:
            url = reverse('admin:network_networknode_change', args=[obj.supplier.pk])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return '-'
    supplier_link.short_description = 'Поставщик (ссылка)'

    def supplier_link_readonly(self, obj):
        return self.supplier_link(obj)
    supplier_link_readonly.short_description = 'Поставщик (ссылка)'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'node', 'release_date')
    list_filter = ('release_date', 'node__name', 'node__city')
    search_fields = ('name', 'model', 'node__name')
    