from django.shortcuts import render
from django.views.generic import ListView
from .models import Table, Booking
# Create your views here.

class TableList(ListView):
    model=Table
    
class BookingList(ListView):
    model=Table
