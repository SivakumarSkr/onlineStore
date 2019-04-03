from django import forms

from .models import Message, Address


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
