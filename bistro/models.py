from django.db import models
from django.conf import settings
from datetime import timedelta
from django.urls import reverse_lazy
# Create your models here.
RESERVED = ((0, 'Free'), (1, 'Reserved'))

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

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
