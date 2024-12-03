from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Product, ProductRange, Site

# Enregistrer les modèles dans l'interface d'administration
admin.site.register(Product)
admin.site.register(ProductRange)

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'product_count', 'is_active')
    list_filter = ('location', 'is_active')
    search_fields = ('name',)
    actions = ['deactivate_sites', 'activate_sites']
    
    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Number of Products'

    def deactivate_sites(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Successfully deactivated {updated} sites.")
    deactivate_sites.short_description = "Deactivate selected sites"

    def activate_sites(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Successfully activated {updated} sites.")
    activate_sites.short_description = "Activate selected sites"

    def delete_model(self, request, obj):
        if obj.can_be_deleted():
            obj.delete()
        else:
            messages.error(request, f"Cannot delete {obj.name} because it has products assigned to it.")

    def delete_queryset(self, request, queryset):
        for site in queryset:
            if site.can_be_deleted():
                site.delete()
            else:
                messages.error(request, f"Cannot delete {site.name} because it has products assigned to it.")
