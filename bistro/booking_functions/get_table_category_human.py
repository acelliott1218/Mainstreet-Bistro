from bistro.models import Table

def get_table_category_human(category):
    '''
    gets the human-readable format from the machine-readable format
    '''
    table = Table.objects.all()[0]
    table_category = dict(table.TABLE_CATEGORIES).get(category, None)
    return table_category

