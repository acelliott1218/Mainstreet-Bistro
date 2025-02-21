from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, FormView, View, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.forms import ModelForm

from .models import Table, Booking, WorkingHour
from .forms import AvailabilityForm
from bistro.booking_functions.booking_validator import validator
from bistro.booking_functions.availability import is_free
from bistro.booking_functions.get_tab_category_list import *
from bistro.booking_functions.get_table_category_human import *
# Create your views here.


def TableListView(request):
    tab_category_list = get_tab_category_list()
    context = {
        'table_list': tab_category_list,
    }
    return render(request, 'table_list_view.html', context)


class BookingList(ListView):
    model = Booking
    template_name = 'booking_list.html'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list


class TableDetailView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        tab_category_human = get_table_category_human(category)
        form = AvailabilityForm()
        user = request.user
        has_booking = Booking.objects.filter(user=user).exists()
        if tab_category_human is not None:
            context = {
                'table_category': tab_category_human,
                'form': form,
                'has_booking': has_booking
            }
            return render(request, 'table_detail_view.html', context)

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
                # to be changed not
                return HttpResponse('All of this category of tables are unavailable')
        else:
            context = {
                'form': form,
                'table_category': get_table_category_human(category),
                'form_errors': form.errors
            }
            return render(request, 'table_detail_view.html', context)


class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('bistro:BookingList')



class BookingEditForm(ModelForm):
    class Meta:
        model = Booking
        fields = ["reservation", "end_time"]

    def clean(self):
        data = super().clean()
        reservation = data.get("reservation")
        end_time = data.get("end_time")

        if not reservation or not end_time:
            return data  # Skip validation if fields are empty

        validator(self, reservation, end_time, data)

class EditBookingView(UpdateView):
    model = Booking
    form_class = BookingEditForm
    template_name = "booking_edit_view.html"
    success_url = reverse_lazy("bistro:BookingList")

    def get_object(self, queryset=None):
        booking = get_object_or_404(Booking, pk=self.kwargs["pk"])
        if booking.user != self.request.user:
            raise PermissionDenied("You cannot edit this booking.")
        return booking


