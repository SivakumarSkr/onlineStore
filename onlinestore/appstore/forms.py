from dal import autocomplete
from django import forms
from django.urls import reverse

from .models import Message, Address, Customer, Product


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'subject', 'message']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        labels = {
            "name": "Name",
            "address": "Address",
            "city": "City/Town",
            "district": "District",
            "pin_code": "PinCode",
            "phone": "Contact No",
            "email": "Email",
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'contact_no', 'profile_pic']
        labels = {
            'name': "Name",
            'contact_no': "Contact number",
            'profile_pic': "Profile Picture",
        }


class Example(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=autocomplete.ModelSelect2(url='http://127.0.0.1/search/')
    )

