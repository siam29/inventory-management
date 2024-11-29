from django.db import models
from django.contrib.gis.db import models as geomodels  # For spatial fields
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils.text import slugify
from uuid import uuid4
import os

class Location(models.Model):
    """
    Location model for storing hierarchical geographic data.
    """
    id = models.CharField(max_length=20, primary_key=True)  # Unique ID
    title = models.CharField(max_length=100)  # Location title
    center = geomodels.PointField()  # Geospatial PointField for location center
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )  # Self-referential foreign key for hierarchical structure
    location_type = models.CharField(
        max_length=20,
        choices=[('country', 'Country'), ('state', 'State'), ('city', 'City')],
        default='city'
    )  # Location type (country, state, city)
    country_code = models.CharField(max_length=2)  # ISO country code
    state_abbr = models.CharField(max_length=3, null=True, blank=True)  # State abbreviation
    city = models.CharField(max_length=30, null=True, blank=True)  # City name
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Last update timestamp

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return f"{self.title} ({self.location_type})"


class Accommodation(models.Model):
    """
    Accommodation model to store details of various properties.
    """
    id = models.CharField(max_length=20, primary_key=True)  # String ID with max length of 20
    feed = models.PositiveSmallIntegerField(default=0)  # Feed number, unsigned small integer
    title = models.CharField(max_length=100)  # Name of the accommodation
    country_code = models.CharField(max_length=2)  # ISO country code
    bedroom_count = models.PositiveIntegerField()  # Number of bedrooms
    review_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)  # Review score (1 decimal place)
    usd_rate = models.DecimalField(max_digits=10, decimal_places=2)  # Price rate in USD
    center = geomodels.PointField()  # Geolocation field
    # images = models.JSONField(null=True, blank=True)  # Array of image URLs
    location = models.ForeignKey('properties.Location', on_delete=models.CASCADE, related_name="accommodations")  # ForeignKey to Location
    # amenities = models.JSONField(null=True, blank=True)  # JSONB array of amenities
    amenities = models.ManyToManyField('Amenity', blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # ForeignKey to Django's auth_user
    published = models.BooleanField(default=False)  # Boolean to indicate if the accommodation is published
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Last update timestamp

    class Meta:
        verbose_name = "Accommodation"
        verbose_name_plural = "Accommodations"

    def __str__(self):
        return f"{self.title} - {self.location.title}"


def upload_accommodation_image(instance, filename):
    """
    Custom upload handler for accommodation images.
    Renames the file to a slugified version with a unique identifier.
    """
    ext = os.path.splitext(filename)[1].lower()
    unique_id = uuid4().hex[:8]
    slugified_name = slugify(os.path.splitext(filename)[0])
    new_filename = f"{slugified_name}-{unique_id}{ext}"
    upload_path = "accommodations/images/"
    upload_path = f"accommodations/{instance.accommodation.id}/images/"
    return os.path.join(upload_path, new_filename)


class AccommodationImage(models.Model):
    accommodation = models.ForeignKey(
        Accommodation,
        on_delete=models.CASCADE,
        related_name='accommodation_images'
    )
    image = models.ImageField(upload_to=upload_accommodation_image)  # Use custom upload function
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.accommodation.title}"

class Amenity(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name or "Unnamed Amenity"

class LocalizeAccommodation(models.Model):
    """
    Localized details for Accommodation, supporting multiple languages.
    """
    id = models.AutoField(primary_key=True)  # Auto-incremented primary key
    accommodation = models.ForeignKey('Accommodation', on_delete=models.CASCADE, related_name='localized')  # Foreign key to Accommodation (accommodation)
    language = models.CharField(max_length=2)  # Language code (ISO 639-1, e.g., 'en', 'es')
    description = models.TextField()  # Localized description
    policy = models.JSONField(null=True, blank=True)  # JSONB policy (e.g., {"pet_policy": "value"})

    class Meta:
        unique_together = ('accommodation', 'language')  # Ensures one translation per language
        verbose_name = "Localized Accommodation"
        verbose_name_plural = "Localized Accommodations"

    def __str__(self):
        return f"{self.localized_name} ({self.language})"