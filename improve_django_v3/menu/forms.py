from django import forms
from django.forms.extras import SelectDateWidget

from .models import Menu, Item


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = [
            'season',
            'items',
            'expiration_date'
        ]
        widgets = {'expiration_date': SelectDateWidget}


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = [
            'name',
            'description',
            'standard',
            'created_date',
            'ingredients'
        ]
        widgets = {'created_date': SelectDateWidget}