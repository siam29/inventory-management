from django.shortcuts import render, get_object_or_404
from .models import Accommodation, LocalizeAccommodation


def localized_accommodation_view(request, accommodation_id, language_code):
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)
    localization = get_object_or_404(LocalizeAccommodation, accommodation=accommodation, language=language_code)

    return render(request, 'localized_accommodation.html', {
        'accommodation': accommodation,
        'localization': localization,
    })
