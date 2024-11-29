from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Location, Accommodation

@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type', 'country_code')


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'price_per_night', 'max_guests', 'available')
    search_fields = ('name', 'location__title')
    list_filter = ('available', 'location')