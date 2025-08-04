from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from django.views import View
from django import forms
from .models import Product
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


class ProductIndexView(View):
    template_name = 'pages/products/index.html'
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.objects.all()
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'pages/products/show.html'

    def get(self, request, id):
        viewData = {}
        try:
            product_id = int(id)
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, Product.DoesNotExist):
            return HttpResponseRedirect(reverse('home'))

        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] = product.name + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']
    description = forms.CharField(required=False)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    
    
class ProductCreateView(View): 
    template_name = 'pages/products/create.html'

    def get(self, request):
        form = ProductForm()
        return render(request, self.template_name, {
            "form": form,
            "title": "Add Product - Online Store"
        })

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  # ✅ Aquí usas form.save() gracias a ModelForm
            return redirect('products.index')
        return render(request, self.template_name, {
            "form": form,
            "title": "Add Product - Online Store"
        })

class ProductListView(ListView): 
    model = Product 
    template_name = 'product_list.html' 
    context_object_name = 'products'  # This will allow you to loop through 'products' in your template 

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context['title'] = 'Products - Online Store' 
        context['subtitle'] = 'List of products' 
        return context  