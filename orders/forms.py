# orders/forms.py

from django import forms
from .models import Order, Item

class OrderForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Order
        fields = ['table_number', 'status', 'items']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price']
