from django.urls import path, include
from .views import TableListView, BookingList, TableDetailView, CancelBookingView

app_name='bistro'

urlpatterns=[
    path('table_list/', TableListView, name='TableList'),
    path('booking_list/', BookingList.as_view(), name='BookingList'),
    path('table/<category>', TableDetailView.as_view(), name="TableDetailView" ),
    path('booking/cancel/<pk>', CancelBookingView.as_view(), name='CancelBookingView'),
    path('appointment/', include('appointment.urls')),
]