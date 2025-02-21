from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import localtime
from .models import WorkingHour
from bistro.booking_functions.booking_validator import validator



class AvailabilityForm(forms.Form):
    reservation = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M%Z"]
    )
    end_time = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M%Z"]
    )

    def clean(self):
        data = super().clean()
        reservation = data.get("reservation")
        end_time = data.get("end_time")

        if not reservation or not end_time:
            return data  # Skip validation if fields are empty
        validator(self, reservation, end_time, data)
