from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, FormView, View
from .models import Table, Booking
from .forms import AvailabilityForm
from bistro.booking_functions.availability import is_free
# Create your views here.

class TableListView(ListView):
    model=Table
    template_name = 'table_list_view.html'
    
class BookingList(ListView):
    model=Booking
    template_name = 'booking_list.html'

class TableDetailView(View):
    def get(self, request, *args, **kwargs):
        table_category = self.kwargs.get('category', None)
        table_list = Table.objects.filter(category=table_category)
        table = table_list[0]
        context ={
            'table_category': table.category
        }
        return render(request, 'table_detail_view.html', context)

    def post(self, request, *args, **kwargs):
        table_list = Table.objects.filter
        available_tables = []
        for table in table_list:
            if is_free(table, data['reservation'], data['end_time']):
                available_tables.append(table)
        if len(available_tables) > 0:
            table = available_tables[0]
            booking = Booking.objects.create(
                user=self.request.user,
                table = table,
                reservation = data['reservation'],
                end_time = data['end_time']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('All of this category of tables are unavailable')

class BookingView(FormView):
    form_class = AvailabilityForm
    template_name = 'availability_form.html'
    
    def form_valid(self, form):
        data = form.cleaned_data
        table_list = Table.objects.filter(category = data['table_category'])
        available_tables = []
        for table in table_list:
            if is_free(table, data['reservation'], data['end_time']):
                available_tables.append(table)
        if len(available_tables) > 0:
            table = available_tables[0]
            booking = Booking.objects.create(
                user=self.request.user,
                table = table,
                reservation = data['reservation'],
                end_time = data['end_time']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('All of this category of tables are unavailable')
