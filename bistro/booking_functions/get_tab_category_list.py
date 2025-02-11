from bistro.models import Table
from django.urls import reverse


def get_tab_category_list():
    '''
    Returns the accurate Table Category and Category URL List
    '''
    table = Table.objects.all()[0]  # gets the initial table object
    # creates a dictionary in human and machine readable format
    table_categories = dict(table.TABLE_CATEGORIES)

    tab_category_list = []  # Creates an empty list to contain Table Category and Table URL

    for category in table_categories:  # populates the aforementioned list
        table_category = table_categories.get(category)
        table_url = reverse('bistro:TableDetailView',
                            kwargs={'category': category})
        tab_category_list.append((table_category, table_url))
    return tab_category_list
