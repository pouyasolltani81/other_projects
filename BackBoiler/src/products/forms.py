from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image_url', 'product_url']

class ScrapeProductForm(forms.Form):
    url = forms.URLField(label='Product URL', widget=forms.URLInput(attrs={'placeholder': 'Enter product URL'}))
