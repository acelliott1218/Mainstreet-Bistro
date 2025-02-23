import datetime
from bistro.models import Table, Booking


def is_free(table, reservation, end_time):
    '''
    checks if the table is actually free, prevents double-booking of a table
    '''

    available = []

    avail_list = Booking.objects.filter(table=table)
    for booking in avail_list:
        if booking.reservation > end_time or booking.end_time < reservation:
            available.append(True)
        else:
            available.append(False)
    return all(available)
