from django.urls import path
from webapp.views import ProductIndex, ProductDetail, ProductCreate, ProductUpdate, ProductDelete, AddItem, CartIndex, CartDelete, OrderCreate

app_name = 'webapp'

urlpatterns = [
    path('', ProductIndex.as_view(), name='product_index'),
    path('product/<int:pk>', ProductDetail.as_view(), name='product_view'),
    path('product/add', ProductCreate.as_view(), name='product_create'),
    path('product/<int:pk>/update', ProductUpdate.as_view(), name='product_update'),
    path('product/<int:pk>/delete', ProductDelete.as_view(), name='product_delete'),
    path('product/<int:pk>/add_to_cart', AddItem.as_view(), name='add_to_cart'),
    path('cart/', CartIndex.as_view(), name='cart_index'),
    path('cart/<int:pk>/delete', CartDelete.as_view(), name='cart_delete'),
    path('order/', OrderCreate.as_view(), name='order_create'),

]
