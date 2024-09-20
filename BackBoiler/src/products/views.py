from django.shortcuts import render, redirect
from .models import Product
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def view_products(request):
    products = Product.objects.all()
    return render(request, 'products/view_products.html', {'products': products})
from django.shortcuts import render, redirect
from .forms import ProductForm, ScrapeProductForm
from .models import Product
from .scraper import scrape_product

def getthechoice(request):
    if request.method == 'POST':
        if 'scrape' in request.POST:
            form = ScrapeProductForm(request.POST)
            if form.is_valid():
                url = form.cleaned_data['url']
                scrape_product(url)
                return redirect('view_products')  
        else:
            name = request.POST['name']
            description = request.POST['description']
            price = request.POST['price']
            image_url = request.POST['image_url']
            product_url = request.POST['product_url']
            Product.objects.create(name=name, description=description, price=price, image_url=image_url, product_url=product_url)
            return redirect('view_products')
    else:
        form = ProductForm()
        scrape_form = ScrapeProductForm()

    return render(request, 'products/main.html', {'form': form, 'scrape_form': scrape_form})


def delete_product(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect('view_products')  

def delete_all_products(request):
    if request.method == 'POST':
        Product.objects.all().delete()  
        return redirect('view_products')  
    


