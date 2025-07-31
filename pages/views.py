from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views import View
from django import forms
# Create your views here.

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
 template_name = 'pages/about.html'

 def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({
        "title": "About us - Online Store",
        "subtitle": "About us",
        "description": "This is an about page ...",
        "author": "Developed by: Your Name",
    })
    return context

class ContactPageView(TemplateView):
    template_name = "pages/contact.html"

class Product:
 products = [
    {"id":"1", "name":"TV", "description":"Best TV", "price": 1299.99},
    {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 1199.99},
    {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 73.59},
    {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 50.25},
    ]
class ProductIndexView(View):
    template_name = 'pages/products/index.html'
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'pages/products/show.html'

    def get(self, request, id):
        viewData = {}
        try:
            product = Product.products[int(id)-1]
        except (IndexError, ValueError):
            return HttpResponseRedirect(reverse('home'))
        
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)

class ProductForm(forms.Form):
    name = forms.CharField(label="Product Name", required=True, max_length=100)
    description = forms.CharField(label="Description", required=True, widget=forms.Textarea)
    price = forms.FloatField(label="Price", required=True)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    
    
class ProductCreateView(View):
    template_name = 'pages/products/create.html'

    def get(self, request):
        form = ProductForm()
        return render(request, self.template_name, {"form": form, "title": "Add Product - Online Store"})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = {
                "id": str(len(Product.products) + 1),
                "name": form.cleaned_data["name"],
                "description": form.cleaned_data["description"],
                "price": form.cleaned_data["price"],
            }
            Product.products.append(new_product)
            return redirect('products.index')  # Asegúrate de tener esta ruta
        return render(request, self.template_name, {"form": form, "title": "Add Product - Online Store"})
