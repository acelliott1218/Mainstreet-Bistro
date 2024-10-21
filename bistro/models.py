from django.db import models

# Create your models here.


class Table(models.Model):
    TABLE_CATEGORIES = (
        ('BTH', 'BOOTH'),
        ('STB', 'STANDARD TABLE'),
        ('PTB', 'PARTY TABLE'),
        ('BTB', 'BANQUET TABLE'),
        ('STL', 'STOOL'),
    )
    number = models.IntegerField()
    category = models.CharField(max_length=3, choices=TABLE_CATEGORIES)
    seats = models.IntegerField()
    capacity = models.IntegerField()
    def __str__(self):
        return f'{self.number}. {self.category} with {self.seats} seats for {self.capacity} people'