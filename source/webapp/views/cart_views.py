from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DeleteView
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


class CartIndex(ListView):
    model = Cart
    template_name = 'cart/cart_index.html'
    context_object_name = 'carts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        total = 0
        for cart in Cart.objects.all():
            total += cart.get_product_total()
        context['total'] = total
        return context


class CartDelete(DeleteView):
    model = Cart
    success_url = reverse_lazy('cart_index')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)