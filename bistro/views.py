from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, View, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.forms import ModelForm

from .models import Table, Booking, WorkingHour
from .forms import AvailabilityForm
from bistro.booking_functions.booking_validator import validator
from bistro.booking_functions.availability import is_free
from bistro.booking_functions.get_tab_category_list import get_tab_category_list
from bistro.booking_functions.get_table_category_human import get_table_category_human
# Create your views here.

def HomeView(request):
    template_name = 'index.html'
    context = {'user':request.user}
    return render(request, "index.html", context)


def TableListView(request):
    '''
    Gets an initial list of tables
    '''
    tab_category_list = get_tab_category_list()
    context = {
        'table_list': tab_category_list,
    }
    return render(request, 'table_list_view.html', context)


class BookingList(LoginRequiredMixin, ListView):
    '''
    Gets a user's bookings, or allows staff members to view all current ones
    '''
    login_url = '/accounts/login/'
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
    '''
    Once a table is selected, this logic handles actually booking the tables.
    Users cannot book more than one table, and must be logged in.
    '''
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        '''
        Gets the actual booking form and table details 
        '''
        category = self.kwargs.get('category', None)
        tab_category_human = get_table_category_human(category) #Makes sure users see the actual table name, instead of (for example) "BTH"
        form = AvailabilityForm() #calls the forms.py logic
        user = request.user
        has_booking = Booking.objects.filter(user=user).exists() #finds the user's bookings, used later to ensure one user can't have multiple ones
        if tab_category_human is not None:
            context = {
                'table_category': tab_category_human,
                'form': form,
                'has_booking': has_booking #only relevant to hide the posting button
            }
            return render(request, 'table_detail_view.html', context)

    def post(self, request, *args, **kwargs):
        '''
        Handles the "submit" button, basically, or post requests if we want to be technical.
        Makes sure the table is available, conforms to AvailabilityForm() logic, and creates
        a booking if everything checks out.
        '''
        category = self.kwargs.get('category', None)
        table_list = Table.objects.filter(category=category)
        form = AvailabilityForm(request.POST)
        user = request.user
        has_booking = Booking.objects.filter(user=user).exists()
        if has_booking:
            form.add_error('reservation', 'You can only have one reservation at a time!')
            context = {
            'form': form,
            'table_category': get_table_category_human(category),
            'form_errors': form.errors
            }
            return render(request,'table_detail_view.html', context)
        if form.is_valid():
            data = form.cleaned_data

            available = []

            for table in table_list: #checks the availability of each table
                if is_free(table, data['reservation'], data['end_time']):
                    available.append(table) #adds the available tables to the available variable
            if len(available) > 0:
                table = available[0] #gives the first available table of the relevant category
                booking = Booking.objects.create(
                    user=self.request.user,
                    table=table,
                    reservation=data['reservation'],
                    end_time=data['end_time']
                )
                booking.save()
                return HttpResponse(booking)
            else:
                # if there aren't available tables, the user is given this instead
                return HttpResponse('All of this category of tables are unavailable')
                #this will be changed from an HttpResponse in the future
        else:
            context = {
                'form': form,
                'table_category': get_table_category_human(category),
                'form_errors': form.errors
            }
            return render(request, 'table_detail_view.html', context) 


class CancelBookingView(DeleteView):
    '''
    Allows users to cancel a booking.
    '''
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('bistro:BookingList')
    def get_object(self, queryset=None):
        '''
        Makes sure the user is actually logged in, prevents
        changing bookings from other users.
        '''
        booking = get_object_or_404(Booking, pk=self.kwargs["pk"])
        if booking.user != self.request.user:
            raise PermissionDenied("You cannot edit this booking.")
        return booking



class BookingEditForm(ModelForm): 
    #credit: staccato on https://stackoverflow.com/questions/17985452/how-do-i-use-updateview
    '''
    Creates a ModelForm, since a regular one wasn't working
    '''
    class Meta:
        model = Booking
        fields = ["reservation", "end_time"]

    def clean(self): #this is just the same logic from forms.py
        data = super().clean()
        reservation = data.get("reservation")
        end_time = data.get("end_time")

        validator(self, reservation, end_time, data)

class EditBookingView(UpdateView):
    '''
    Works basically the same as cancelling, code-wise, but
    updates the booking instead.
    '''
    model = Booking
    form_class = BookingEditForm
    template_name = "booking_edit_view.html"
    success_url = reverse_lazy("bistro:BookingList")

    def get_object(self, queryset=None):
        '''
        Makes sure the user is actually logged in, prevents
        changing bookings from other users.
        '''
        booking = get_object_or_404(Booking, pk=self.kwargs["pk"])
        #from https://www.reddit.com/r/django/comments/ebbsrn/how_to_limit_users_to_only_edit_their_own_posts/
        if booking.user != self.request.user:
            raise PermissionDenied("You cannot edit this booking.")
        return booking


