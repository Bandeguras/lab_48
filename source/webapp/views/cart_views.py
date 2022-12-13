from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from webapp.models import Products, Cart


class CartView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.all()
        product = cart.product = get_object_or_404(Products, pk=self.kwargs.get('pk'))
        Cart.remains += 1
        context = {
            'cart': cart,
            'product': product
        }

        return render(request, 'cart/cart_index.html', context)
