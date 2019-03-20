from django.urls import path
from .views import *

app_name = 'online'
urlpatterns = [
    path('', view, name='home'),
    path('product/', product, name='product'),
    path('cart/', cart, name='cart'),
    path('category/', category, name='category'),
    path('checkout/', checkout, name='checkout'),
    path('contact/', contact, name='contact'),
]