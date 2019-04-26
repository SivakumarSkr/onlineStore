from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class OrderSerializers(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        fields = ('url', 'date', 'amount', 'payment_success')

