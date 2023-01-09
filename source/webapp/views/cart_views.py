from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DeleteView, CreateView
from webapp.models import Products, Cart, Order, OrderProduct
from webapp.form import OrderForm


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
        return redirect('webapp:product_index')


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
        context['form'] = OrderForm

        return context


class CartDelete(DeleteView):
    model = Cart
    success_url = reverse_lazy('webapp:cart_index')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('webapp:product_index')

    def form_valid(self, form):
        order = form.save()

        for item in Cart.objects.all():
            OrderProduct.objects.create(product=item.product, remains=item.remains, order=order)
            item.product.remains -= item.remains
            item.product.save()
            item.delete()

        return redirect(self.success_url)