from django.urls import path
from .views import *

app_name = 'online'
urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('product/<int:pk>/', ProductDet.as_view(), name='product'),
    path('cart/', cart, name='cart'),
    path('category/', CategoryList.as_view(), name='category'),
    path('checkout/', checkout, name='checkout'),
    path('contact/', contact, name='contact'),
    path('subcategories/', subcategory, name='subcategory'),
    path('sign_up/', sign_up, name='signup'),
    path('cartcreate/<int:pk>/', cart_create, name='cartitemcreate'),
]