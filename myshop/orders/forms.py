from django import forms
from .models import Order, ShippingMethod

class OrderCreateForm(forms.ModelForm):
    shipping_method_obj = forms.ModelChoiceField(
        queryset=ShippingMethod.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'shipping-select'}),
        label="Способ доставки",
        empty_label=None
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'payment_method', 'address'] 
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ivan@example.com'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Улица, дом, квартира'}),
            'payment_method': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }