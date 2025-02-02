from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, FormView, View
from django.urls import reverse
from .models import Table, Booking
from .forms import AvailabilityForm
from bistro.booking_functions.availability import is_free
# Create your views here.

def TableListView(request):
    table = Table.objects.all()[0]
    table_categories = dict(table.TABLE_CATEGORIES)
    table_values = table_categories.values()
    table_list=[]
    for table_category in table_categories:
        table = table_categories.get(table_category)
        table_url = reverse('bistro:TableDetailView', kwargs={'category': table_category})
        table_list.append((table, table_url))
    context={
        'table_list':table_list,
    }
    return render(request, 'table_list_view.html', context)
    
class BookingList(ListView):
    model=Booking
    template_name = 'booking_list.html'
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list

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
