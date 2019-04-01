from django.urls import path
from .views import *

app_name = 'online'
urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('products/<int:pk>/', ProductDet.as_view(), name='product'),
    path('cart/', CartList.as_view(), name='cart'),
    path('category/<int:pk>/', CategoryDetail.as_view(), name='category'),
    path('checkout/', checkout, name='checkout'),
    path('contact/', contact, name='contact'),
    path('subcategories/', subcategory, name='subcategory'),
    path('sign_up/', sign_up, name='signup'),
    path('cartcreate/<int:pk>/', cart_create, name='cartitemcreate'),
    path('deleteorderitem/<int:pk>/', delete_item, name='deleteitem'),
    path('deletecart/', clear_cart, name='clearcart'),
    path('ajax/get_number/', get_no_items, name='get_number'),
]