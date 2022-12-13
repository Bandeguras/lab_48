from django import forms
from webapp.models import Products
from django.forms import widgets
CATEGORY_CHOICES = [('other', 'Разное'), ('vegetables', 'Овощи'), ('Fruit', 'Фрукты'), ('cereals', 'Крупы'), ('meat', 'Мясо')]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'description', 'category', 'remains', 'price']


class Search(forms.Form):
    search = forms.CharField(max_length=50, required=False, label="Search")
