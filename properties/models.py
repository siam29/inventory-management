from django.db import models
from django.contrib.gis.db import models as geomodels  # For spatial fields
from django.core.validators import MinValueValidator
from decimal import Decimal

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
    id = models.AutoField(primary_key=True)  # Auto-incremented ID
    name = models.CharField(max_length=150)  # Accommodation name
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="accommodations")  # ForeignKey to Location
    description = models.TextField(null=True, blank=True)  # Description of the accommodation
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])  # Price per night
    max_guests = models.PositiveIntegerField()  # Maximum number of guests allowed
    available = models.BooleanField(default=True)  # Availability status
    amenities = models.JSONField(null=True, blank=True)  # List of amenities as a JSON field
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Last update timestamp

    def __str__(self):
        return f"{self.name} - {self.location.title}"