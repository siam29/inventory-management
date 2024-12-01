from django.urls import path
from . import views
from .views import my_properties, update_accommodation

urlpatterns = [
    path('', views.home, name='home'), 
    path('accommodation/<int:accommodation_id>/<str:language_code>/', 
         views.localized_accommodation_view, name='localized_accommodation'),

    path('my-properties/', my_properties, name='my_properties'),
    path('accommodation/<int:pk>/update/', update_accommodation, name='update_accommodation'),
]
