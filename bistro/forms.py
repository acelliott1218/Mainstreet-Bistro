from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import localtime
from .models import WorkingHour


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

        now = timezone.now()

        # Ensure reservation is in the future
        if reservation < now:
            self.add_error('reservation', 'Reservation date cannot be in the past.')

        # Ensure end_time is after reservation
        if end_time <= reservation:
            self.add_error('end_time', 'End time must be after the reservation start time.')

        # Get working hours for the selected day
        working_hours = WorkingHour.objects.filter(day=reservation.weekday()).first()

        if not working_hours:
            self.add_error('reservation', 'No reservations allowed on this day.')
        else:
            # Ensure reservation falls within working hours
            if not (working_hours.start_time <= reservation.time() <= working_hours.end_time):
                self.add_error('reservation', f'Reservations must be between {working_hours.start_time} and {working_hours.end_time}.')
            if not (working_hours.start_time <= end_time.time() <= working_hours.end_time):
                self.add_error('end_time', f'Reservations must end by {working_hours.end_time}.')

        # Restrict booking duration (30 min - 3 hours)
        total_res = (end_time - reservation).total_seconds()
        if not (1800 <= total_res <= 10800):  # 30 minutes (1800s) - 3 hours (10800s)
            self.add_error('end_time', 'Reservations must last at least 30 minutes, and at most 3 hours.')

        return data