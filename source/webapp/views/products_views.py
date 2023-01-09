from django.db.models import Q
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from webapp.models import Products
from webapp.form import ProductForm, Search
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
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


class ProductCreate(PermissionRequiredMixin, CreateView):
    template_name = 'product/create.html'
    model = Products
    context_object_name = 'product'
    form_class = ProductForm
    permission_required = 'webapp.add_products'
    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'product/update.html'
    model = Products
    context_object_name = 'product'
    form_class = ProductForm
    permission_required = 'webapp.change_products'

    def get_queryset(self):
        return Products.objects.all().filter(remains__gt=0)

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'product/delete.html'
    model = Products
    context_object_name = 'product'
    permission_required = 'webapp.delete_products'

    def get_queryset(self):
        return Products.objects.all().filter(remains__gt=0)

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.product.pk})

