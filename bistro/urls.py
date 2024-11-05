from django.urls import path
from .views import TableListView, BookingList, BookingView, TableDetailView

app_name='bistro'

urlpatterns=[
    path('table_list/', TableListView.as_view(), name='TableList'),
    path('booking_list/', BookingList.as_view(), name='BookingList'),
    path('book/', BookingView.as_view(), name='BookingView'),
    path('table/<category>', TableDetailView.as_view(), name="TableDetailView" )
]