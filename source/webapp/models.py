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
    product = models.ForeignKey('webapp.Products', on_delete=models.CASCADE, related_name='cart', verbose_name='Товар')
    remains = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.product.name} - {self.remains}'

    def get_product_total(self):
        return self.remains * self.product.price


class OrderProduct(models.Model):
    product = models.ForeignKey('webapp.Products', on_delete=models.CASCADE, verbose_name='Товар')
    order = models.ForeignKey('webapp.Order', on_delete=models.CASCADE, verbose_name='Заказ')
    remains = models.PositiveIntegerField(verbose_name='Количество')


class Order(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name='Имя пользователя')
    phone = models.CharField(max_length=100, blank=False, null=False, verbose_name='Телефон')
    address = models.CharField(max_length=100, blank=False, null=False, verbose_name='Адрес')
    crated_add = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    product = models.ManyToManyField('webapp.Products', related_name='order', through='webapp.OrderProduct', through_fields=['order', 'product'], verbose_name='Товары')
