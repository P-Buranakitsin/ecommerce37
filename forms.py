from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    product_name = forms.CharField(max_length=100)
    quantity = forms.IntegerField(min_value=1)

