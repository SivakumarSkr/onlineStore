from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageForm, AddressForm
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import *

from .models import *


def view(request):
    return render(request, 'index.html')


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['index_list'] = Product.objects.all()
        return context


class CategoryList(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'category'

    def get_queryset(self):

        return Category.objects.all()


class CategoryDetail(DetailView):
    model = Category
    template_name = 'subcategories.html'
    context_object_name = 'category'


class SubCategoryDetail(DetailView):
    model = SubCategory
    template_name = 'subcategories.html'
    context_object_name = 'subcategory'


class ProductDet(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'prod'


class CartList(ListView):
    model = OrderItem
    template_name = 'cart.html'
    context_object_name = 'cart'

    def get_queryset(self):
        return OrderItem.objects.all()


def cart_create(request, pk):
    obj = OrderItem()
    obj.item = Product.objects.get(pk=pk)
    obj.no_of_items = 0
    obj.total = 0
    obj.save()
    return redirect('online:cart')


class Order(ListView):
    model = Order
    template_name = ''
    context_object_name = 'order'

    def get_queryset(self):
        pass


class OrderDetail(DetailView):
    model = Order
    template_name = ''
    context_object_name = 'orderd'


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            u = form.cleaned_data.get('username')
            p = form.cleaned_data.get('password1')
            user = authenticate(username=u, password=p)
            login(request, user)
            return redirect('online:home')
        else:
            return render(request, 'registration/signup.html', {'form': form})
    else:

        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})


def delete_item(request, pk):
    obj = OrderItem.objects.get(id=pk)
    obj.delete()
    return redirect('online:cart')


def clear_cart(request):
    obj_list = OrderItem.objects.filter(order__isnull=True)
    for i in obj_list:
        i.delete()
    return redirect('online:cart')


def get_no_items(request):
    data = {
        'number': OrderItem.objects.count()
    }
    return JsonResponse(data)


def update_cart(request):
    pk = request.GET.get('primaryKey')
    quantity = request.GET.get('quantity')
    total = request.GET.get('total')
    item = get_object_or_404(OrderItem, pk=pk)
    item.no_of_items = quantity
    item.total = total

    item.save()
    data = {
        'status': 'ok',
    }
    return JsonResponse(data)


class MessageCreate(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'contact.html'
    success_url = reverse_lazy('online:home')


class AddressCreate(CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'checkout.html'
    success_url = reverse_lazy('online:home')

