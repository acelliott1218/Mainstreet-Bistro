from django import forms
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
        validator(self, reservation, end_time, data)
