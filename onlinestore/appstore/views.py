from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import *

from .models import *


def view(request):
    return render(request, 'index.html')


# def product(request):
#     return render(request, 'product.html')
#



def category(request):
    return render(request, 'categories.html')


def checkout(request):
    return render(request, 'checkout.html')


def contact(request):
    return render(request, 'contact.html')


def subcategory(request):
    return render(request, 'subcategories.html')


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
    queryset = Category.objects.all()


class CategoryDetail(DetailView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'category'


class SubCategoryDetail(DetailView):
    model = SubCategory
    template_name = 'categories.html'
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
    obj.no_of_items = 1
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

class