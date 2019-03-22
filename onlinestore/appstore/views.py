from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import *

from .models import *


def view(request):
    return render(request, 'index.html')


def product(request):
    return render(request, 'product.html')


def cart(request):
    return render(request, 'cart.html')


def category(request):
    return render(request, 'categories.html')


def checkout(request):
    return render(request, 'checkout.html')


def contact(request):
    return render(request, 'contact.html')


def subcategory(request):
    return render(request, 'subcategories.html')


class CategoryList(ListView):
    model = Category
    template_name = 'appstore/categorylist.html'
    context_object_name = 'category'
    queryset = Category.objects.all()


class CategoryDetail(DetailView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'category'


class SubCategoryDetail(DetailView):
    model = SubCategory
    template_name = 'categories.html'
    context_object_name = 'subcategory'


class Product(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'prod'


class CartList(ListView):
    model = OrderItem
    template_name = 'cart.html'
    context_object_name = 'cart'

    def get_queryset(self):
        pass


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
    if 'sign-up' in request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            u = form.cleaned_data.get('username')
            p = form.cleaned_data.get('password1')
            user = authenticate(username=u, password=p)

            return redirect('foodchain:customercreate', pk=user.id)
        else:
            return render(request, 'registration/login.html', {'form1': form})
    else:

        form = UserCreationForm()
        return render(request, 'registration/login.html', {'form1': form})
