from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import urlencode

from webapp.models import Products
from webapp.form import ProductForm, Search
from django.views.generic import ListView, DetailView, CreateView
# Create your views here.


class ProductIndex(ListView):
    template_name = 'product/index.html'
    context_object_name = 'products'
    model = Products
    ordering = 'name', 'category'

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return Search(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(remains__gt=0)
        if self.search_value:
            queryset = queryset.filter(Q(name__icontains=self.search_value) | Q(category__icontains=self.search_value))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            context['search'] = self.search_value
        return context


class ProductDetail(DetailView):
    template_name = 'product/view.html'
    model = Products
    context_object_name = 'product'

    def get_queryset(self):
        return Products.objects.all().filter(remains__gt=0)


class ProductCreate(CreateView):
    template_name = 'product/create.html'
    model = Products
    context_object_name = 'product'
    form_class = ProductForm

    def get_queryset(self):
        return Products.objects.all().filter(remains__gt=0)

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.product.pk})

    def form_valid(self, form):
        product = get_object_or_404(Products, pk=self.kwargs.get('pk'))
        form.instance.product = product
        return super().form_valid(form)

def update_product_view(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'GET':
        form = ProductForm(initial={
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'remains': product.remains,
            'price': product.price,
        })
        return render(request, 'product/update.html', {'form': form})

    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.name = form.cleaned_data.get('name')
            product.description = form.cleaned_data.get('description')
            product.category = form.cleaned_data.get('category')
            product.remains = form.cleaned_data.get('remains')
            product.price = form.cleaned_data.get('price')
            product.save()
            return redirect('view', pk)
        else:
            return render(request, 'product/update.html', {'form': form})


def delete_product_view(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'GET':
        return render(request, 'product/delete.html', {'product': product})
    elif request.method == 'POST':
        product.delete()
        return redirect('index')
