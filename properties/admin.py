from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Location, Accommodation, AccommodationImage, LocalizeAccommodation

@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type', 'country_code')


class AccommodationImageInline(admin.TabularInline):
    """
    Inline admin for managing images related to an Accommodation.
    """
    model = AccommodationImage
    extra = 1  # Number of empty slots to display for adding new images
    fields = ('image',)  # Fields to display in the inline
    readonly_fields = ('uploaded_at',)


@admin.register(Accommodation)
class AccommodationAdmin(LeafletGeoAdmin):
    list_display = ('id', 'title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'center', 'location', 'published', 'created_at', 'updated_at')
    list_filter = ('published', 'location') 
    search_fields = ('title', 'country_code', 'location__title')
    ordering = ('-created_at',)
    inlines = [AccommodationImageInline]  # Add the inline for managing images


@admin.register(AccommodationImage)
class AccommodationImageAdmin(admin.ModelAdmin):
    """
    Admin interface for the AccommodationImage model.
    """
    list_display = ('accommodation', 'image', 'uploaded_at')
    search_fields = ('accommodation__title',)

# @admin.register(Amenity)
# class AmenityAdmin(admin.ModelAdmin):
#     list_display = ('name',)  # Optional, for better display in the admin

@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'accommodation', 'language', 'description')
    list_filter = ('language',)
    search_fields = ('description', 'language')