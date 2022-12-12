from django import forms
from django.forms import widgets
CATEGORY_CHOICES = [('other', 'Разное'), ('vegetables', 'Овощи'), ('Fruit', 'Фрукты'), ('cereals', 'Крупы'), ('meat', 'Мясо')]


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, label="Название", required=True)
    description = forms.CharField(max_length=2000, label="Описание", required=False,
                                  widget=widgets.Textarea(attrs={"cols": 20, "rows": 3}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label="Категория", required=True)
    remains = forms.IntegerField(min_value=0, label='Остаток')
    price = forms.DecimalField(max_digits=7, decimal_places=2, label='Цена')


class Search(forms.Form):
    search = forms.CharField(max_length=50, required=False, label="Search")
