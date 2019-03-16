from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import *

from .models import *


def view(request):
    return HttpResponse('hello')


class CategoryList(ListView):
    model = Category
    template_name = 'appstore/categorylist.html'
    context_object_name = 'category'
    queryset = Category.objects.all()


class CategoryDetail(DetailView):
    model = Category
    template_name = 'appstore/categorydetail.html'
    context_object_name = 'category_d'


class SubCategoryList(ListView):
    model = SubCategory
    template_name = 'appstore/subcategorylist.html'
    context_object_name = 'subcategory'
    queryset = SubCategory.objects.all()


class SubCategoryDetail(DetailView):
    model = SubCategory
    template_name = 'appstore/subcategorydetail.html'
    context_object_name = 'subcategory'


class ProductList(ListView):
    model = Product
    template_name = 'appstore/productlist.html'
    context_object_name = 'product'
    queryset = Product.objects.all()


class Product
