from django import forms

class AvailabilityForm(forms.Form):
    TABLE_CATEGORIES = (
        ('BTH', 'BOOTH'),
        ('STB', 'STANDARD TABLE'),
        ('PTB', 'PARTY TABLE'),
        ('BTB', 'BANQUET TABLE'),
        ('STL', 'STOOL'),
    )

    table_category = forms.ChoiceField(choices=TABLE_CATEGORIES, required=True)
    reservation = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M%Z",])
    end_time = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M%Z",])    