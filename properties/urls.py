from django.urls import path
from . import views

urlpatterns = [
    path('accommodation/<int:accommodation_id>/<str:language_code>/', 
         views.localized_accommodation_view, name='localized_accommodation'),
]
