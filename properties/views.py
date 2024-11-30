from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from .models import Accommodation, LocalizeAccommodation
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.decorators import login_required



def home(request):
    return HttpResponse("Welcome to the Home Page!")

def localized_accommodation_view(request, accommodation_id, language_code):
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)
    localization = get_object_or_404(LocalizeAccommodation, accommodation=accommodation, language=language_code)

    return render(request, 'localized_accommodation.html', {
        'accommodation': accommodation,
        'localization': localization,
    })

@login_required
def my_properties(request):
    """
    View for Property Owners to manage their own properties.
    """
    properties = Accommodation.objects.filter(user=request.user)
    return render(request, 'properties/my_properties.html', {'properties': properties})

@login_required
def update_accommodation(request, pk):
    """
    Update accommodation details, restricted to the property owner.
    """
    accommodation = get_object_or_404(Accommodation, pk=pk)

    if accommodation.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this property.")

    # Logic to update accommodation...
    return render(request, 'properties/update_accommodation.html', {'accommodation': accommodation})