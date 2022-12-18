from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View
from webapp.models import Products, Cart


class AddItem(View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Products, pk=self.kwargs.get('pk'))
        try:
            cart = Cart.objects.get(product=product)
            if cart.remains < product.remains:
                cart.remains += 1
                cart.save()
        except Cart.DoesNotExist:
            if product.remains > 0:
                Cart.objects.create(product=product, remains=1)
        return redirect('product_index')