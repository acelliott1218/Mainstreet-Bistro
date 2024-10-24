from django.urls import path
from .views import TableList, BookingList, BookingView

app_name='bistro'

urlpatterns=[
    path('booking_list/', BookingList.as_view(), name='BookingList'),
    path('table_list/', TableList.as_view(), name='TableList'),
    path('book/', BookingView.as_view(), name='booking_view')
]