from django.contrib import admin
from .models import Service, Category # Importe os modelos Service e Category

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'billing_model', 'price', 'display_formatted_price') # Referencie o método aqui
    search_fields = ('name', 'category__name', 'billing_model')
    readonly_fields = ('display_formatted_price',) # Referencie o método aqui

    # Defina o método DENTRO da classe ServiceAdmin
    def display_formatted_price(self, obj):
        return obj.formatted_price # Ele ainda chama a propriedade 'formatted_price' do seu modelo

    # Aplique short_description e admin_order_field AO MÉTODO 'display_formatted_price'
    display_formatted_price.short_description = 'Preço (R$)'
    display_formatted_price.admin_order_field = 'price'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    


 
