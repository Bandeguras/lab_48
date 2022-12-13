from django.db import models

# Create your models here.

CATEGORY_CHOICES = [('other', 'Разное'), ('vegetables', 'Овощи'), ('Fruit', 'Фрукты'), ('cereals', 'Крупы'), ('meat', 'Мясо')]


class Products(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(max_length=2000, verbose_name="Описание", null=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES[0][0], verbose_name="Категория")
    remains = models.PositiveIntegerField(verbose_name='Остаток')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')


class Cart(models.Model):
    product = models.ForeignKey('webapp.Products', on_delete=models.CASCADE, related_name='products')
    remains = models.PositiveIntegerField(verbose_name='Количество')
