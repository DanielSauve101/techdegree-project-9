from django import forms
from django.forms.extras import SelectDateWidget

from .models import Menu, Item, Ingredient


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = [
            'season',
            'items',
            'expiration_date'
        ]
        widgets = {'expiration_date': SelectDateWidget}