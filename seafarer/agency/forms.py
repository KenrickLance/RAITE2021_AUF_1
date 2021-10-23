from django.forms import ModelForm
from .models import Crew, Ship, Charter

class CrewCreationForm(ModelForm):
    class Meta:
        model = Crew
        fields = ['first_name', 'last_name', 'middle_name',
                  'phone', 'email', 'sex', 'birth_date', 'address', 'country_of_residence',
                  'position'
        ]

class ShipCreationForm(ModelForm):
    class Meta:
        model = Ship
        fields = ['name', 'speed_class', 'IMO', 'vessel_type',
                 'status', 'call_sign', 'flag', 'gross_tonnage',
                 'summer_dwt', 'length_overall', 'breadth_extreme',
                 'year_built', 'home_port']

class CharterCreationForm(ModelForm):
    class Meta:
        model = Charter
        exclude = ['from_datetime', 'to_datetime']
