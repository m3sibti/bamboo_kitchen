from django.forms import ModelForm
from .models import *


class StockItemForm(ModelForm):
    class Meta:
        model = StockItem
        fields = ['name']


class StockForm(ModelForm):
    class Meta:
        model = Stock
        exclude = ('date_created', 'add_by')


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class MenuItemForm(ModelForm):
    class Meta:
        model = MenuItem
        exclude = ('date_created', 'add_by')


class DealForm(ModelForm):
    class Meta:
        model = Deal
        fields = ['name', 'price']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ('charges', 'bill', 'date_created', 'add_by')


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        exclude = ('order',)
