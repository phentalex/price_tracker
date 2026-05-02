from django import forms

from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['url', 'target_price']
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'target_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }