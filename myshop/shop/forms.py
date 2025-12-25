from django import forms

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control text-center', 'style': 'width: 70px;'}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)