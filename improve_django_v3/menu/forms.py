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

    def clean(self):
        cleaned_data = super().clean()
        season = cleaned_data.get('season')
        seasons = ['winter', 'spring', 'summer', 'fall']

        if not any(x in season.lower() for x in seasons):
            raise forms.ValidationError(
                "Must include a season. 'Winter, Spring, Summer, or Fall.'"
                )


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
        widgets = {
            'created_date': SelectDateWidget,
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 5})
            }
