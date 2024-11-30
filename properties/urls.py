from django.urls import path
from . import views
from .views import my_properties, update_accommodation

urlpatterns = [
    path('', views.home, name='home'), 
    path('accommodation/<int:accommodation_id>/<str:language_code>/', 
         views.localized_accommodation_view, name='localized_accommodation'),

    path('my-properties/', my_properties, name='my_properties'),
    path('accommodation/<int:pk>/update/', update_accommodation, name='update_accommodation'),


    # path('locations/', views.LocationListView.as_view(), name='location_list'),
    # path('locations/<str:pk>/', views.LocationDetailView.as_view(), name='location_detail'),
    # path('accommodations/', views.AccommodationListView.as_view(), name='accommodation_list'),
    # path('accommodations/<str:pk>/', views.AccommodationDetailView.as_view(), name='accommodation_detail'),
    # path('localize/', views.LocalizeAccommodationListView.as_view(), name='localize_accommodation_list'),
    # path('localize/<int:pk>/', views.LocalizeAccommodationDetailView.as_view(), name='localize_accommodation_detail'),
]
