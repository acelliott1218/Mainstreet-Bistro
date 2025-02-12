from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


class AvailabilityForm(forms.Form):
    reservation = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M%Z",])
    end_time = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M%Z",])

    def clean(self):
        data = super().clean()

        reservation = data.get("reservation")
        end_time = data.get("end_time")

        total_res = (end_time - reservation).total_seconds() #uses total seconds to ensure an accurate time-count

        max_res = 10800 #3 hours
        min_res = 1800 #30 minutes

        now = timezone.now() #created for readability, basically
        if end_time <= reservation or reservation < now: #makes sure the user can't time travel
            self.add_error('reservation', 'Reservation date cannot be in the past.')
        elif total_res > max_res or total_res < min_res: #ensures a minimal and maximal limit to the reservation
            self.add_error('end_time', 'Reservations must last at least 30 minutes, and at most 3 hours.')
        return data