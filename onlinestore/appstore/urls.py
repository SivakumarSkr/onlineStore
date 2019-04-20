from django.urls import path
from .views import *

app_name = 'online'
urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('products/<int:pk>/', ProductDet.as_view(), name='product'),
    path('cart/', CartList.as_view(), name='cart'),
    path('category/<int:pk>/', CategoryDetail.as_view(), name='category'),
    path('checkout/<int:pk>/', AddressCreate.as_view(), name='checkout'),
    path('sign_up/', sign_up, name='signup'),
    path('cartcreate/<int:pk>/', cart_create, name='cartitemcreate'),
    path('deleteorderitem/<int:pk>/', delete_item, name='deleteitem'),
    path('deletecart/', clear_cart, name='clearcart'),
    path('ajax/get_number/', get_no_items, name='get_number'),
    path('ajax/updatecart/', update_cart, name='updatecart'),
    path('ajax/getcheck/', check_cart, name='checkcart'),
    path('ajax/get_total/', get_total, name='gettotal'),
    path('categories/', CategoryList.as_view(), name='categorylist'),
    path('message_create/', MessageCreate.as_view(), name='message_create'),
    path('order_create/', order_create, name='order_create'),
    path('autocompleteview/', ProductAutoComplete.as_view(), name='productautocomplete'),
    path('search/', ProductSearch.as_view(), name='search'),
    path('customercreate/', CustomerCreation.as_view(), name='customercreate'),
    path('profile/<int:pk>/', Profile.as_view(), name='profile'),
    path('orders/', OrderList.as_view(), name='orderlist'),
    path('paymentconfirm/<int:pk>/', payment_success, name='paymentsuccess'),
    path('ordersummary/<int:pk>/', OrderSummary.as_view(), name='ordersummary'),
    path('payment_create/<int:pk>/', payment_request, name='payment-create'),
]
