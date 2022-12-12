from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import Products
from webapp.form import ProductForm
# Create your views here.


def index_view(request):
    products = Products.objects.all().filter(remains__gt=0).order_by('name', 'category')
    search_products = request.GET.get('search')
    if search_products:
        products = Products.objects.all().filter(name=search_products, remains__gt=0).order_by('name', 'category')
        context = {
            'products': products,
        }
        return render(request, 'index.html', context)
    context = {'products': products}
    return render(request, 'index.html', context)


def product_view(request, pk):
    product = get_object_or_404(Products, pk=pk)
    context = {'product': product}
    return render(request, 'view.html', context)


def create_view(request):
    if request.method == 'GET':
        form = ProductForm()
        return render(request, "create.html", {'form': form})
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            new_product = Products.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                category=form.cleaned_data['category'],
                remains=form.cleaned_data['remains'],
                price=form.cleaned_data['price'],

            )
            return redirect('view', pk=new_product.pk)
        else:
            return render(request, "create.html", {'form': form})


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
        return render(request, 'update.html', {'form': form})

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
            return render(request, 'update.html', {'form': form})


def delete_product_view(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete.html', {'product': product})
    elif request.method == 'POST':
        product.delete()
        return redirect('index')
