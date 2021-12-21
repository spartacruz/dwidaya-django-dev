from django import forms
from django.forms import models
from .models import Customer


class FlightForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('flightfrom', 'flightto', 'departuredate', 'returndate', 
        'firstname', 'lastname', 'mobile', 'email')

        labels = {
            'flightfrom': 'Flight From',
            'flightto': 'Flight To',
            'departuredate': 'Departure Date',
            'returndate': 'Return Date',
            'firstname': 'First Name',
            'lastname': 'Last Name',
            'mobile': 'Mobile Phone Number',
            'email': 'Email'
        }

    def __init__(self, *args, **kwargs):
        super(FlightForm, self).__init__(*args, **kwargs)
        self.fields['flightfrom'].empty_label = "Select"
        self.fields['flightto'].empty_label = "Select"

        self.fields['departuredate'].widget.attrs['placeholder'] = '31-12-2021'
        self.fields['returndate'].widget.attrs['placeholder'] = '31-12-2021'

        self.fields['firstname'].widget.attrs['placeholder'] = 'John'
        self.fields['lastname'].widget.attrs['placeholder'] = 'Doe'

        self.fields['mobile'].widget.attrs['placeholder'] = '081288068052'
        self.fields['email'].widget.attrs['placeholder'] = 'john@doe.com'
        # self.fields['returndate'].required = False