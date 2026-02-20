from django.contrib import admin
from .models import Booking , CarBrand, CarModel

class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')
    search_fields = ('name', 'brand__name')


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [CarModelInline]
    
    

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    
    autocomplete_fields = ['car_model']
      
    list_display = (
        'customer_name',
        'car_brand',
        'car_model',
        'fuel_type',
        'service_date',
        'status'
    )

    list_filter = (
        'status',
        'fuel_type',
        'service_date',
    )

    search_fields = (
        'customer_name',
        'car_brand',
        'car_model',
    )

    ordering = ('-created_at',)


