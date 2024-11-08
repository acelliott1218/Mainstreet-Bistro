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
        category = self.kwargs.get('category', None)
        form = AvailabilityForm()
        table_list = Table.objects.filter(category=category)

        if len(table_list) > 0:
            table = table_list[0]
            table_category = dict(table.TABLE_CATEGORIES).get(table.category, None)
            context = {
                'table_category': table_category,
                'form': form,
            }
            return render(request, 'table_detail_view.html', context)
        else:
            return HttpResponse('Category does not exist')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        table_list = Table.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            
            available = []
            for table in table_list:
                if is_free(table, data['reservation'], data['end_time']):
                    available.append(table)
            if len(available) > 0:
                table = available[0]
                booking = Booking.objects.create(
                    user=self.request.user,
                    table=table,
                    reservation=data['reservation'],
                    end_time=data['end_time']
                )
                booking.save()
                return HttpResponse(booking)
            else:
                return HttpResponse('All of this category of tables are unavailable')
        else:
            return HttpResponse(f'Invalid form data: {form.errors}')

class BookingView(FormView):
    form_class = AvailabilityForm
    template_name = 'availability_form.html'
    
    def form_valid(self, form):
        data = form.cleaned_data
        table_list = Table.objects.filter(category = data['table_category'])
        available = []
        for table in table_list:
            if is_free(table, data['reservation'], data['end_time']):
                available.append(table)
        if len(available) > 0:
            table = available[0]
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
