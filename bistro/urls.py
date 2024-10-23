from django.urls import path
from .views import TableList, BookingList

app_name='bistro'

urlpatterns=[
    path('table_list/', TableList.as_view(), name='TableList'),
    path('booking_list/', BookingList.as_view(), name='BookingList'),
]