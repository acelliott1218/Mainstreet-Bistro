from django.db import models
from django.conf import settings
from datetime import timedelta
from django.urls import reverse_lazy

# Create your models here.


class Table(models.Model):
    TABLE_CATEGORIES = (
        ('BTH', 'BOOTH'),
        ('STB', 'STANDARD TABLE'),
        ('PTB', 'PARTY TABLE'),
        ('BTB', 'BANQUET TABLE'),
    )
    number = models.IntegerField()
    category = models.CharField(max_length=3, choices=TABLE_CATEGORIES)
    seats = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        return f'{self.number}. {self.category} with {self.seats} seats for {self.capacity} people'


class WorkingHour(models.Model):
    '''
    Allows post-launch updates to working hours. Will be changed to use calendar logic instead in the future.
    '''
    DAY_CHOICES = (
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    )
    OPEN_CLOSED = (
        (0, "Yes"),
        (1, "No")
    )
    day = models.IntegerField(choices=DAY_CHOICES, unique=True)
    availability = models.IntegerField(choices=OPEN_CLOSED, default=0)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        day_name = dict(self.DAY_CHOICES).get(self.day)
        if self.availability == 1:
            return f"Closed on {day_name}."
        return f"Open on {day_name} from {self.start_time} to {self.end_time}"


class Booking(models.Model):
    '''
    Exists to actually allow the bookings in the first place.
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    reservation = models.DateTimeField()
    end_time = models.DateTimeField(default=None)

    def __str__(self):
        return f'{self.user} has reserved {self.table} for {self.reservation}.'

    def get_table_category(self):
        table_categories = dict(self.table.TABLE_CATEGORIES)
        table_category = table_categories.get(self.table.category)
        return table_category

    def get_cancel_booking_url(self):
        return reverse_lazy('bistro:CancelBookingView', args=[self.pk, ])

    def get_edit_booking_url(self):
        return reverse_lazy('bistro:EditBookingView', args=[self.pk, ])
