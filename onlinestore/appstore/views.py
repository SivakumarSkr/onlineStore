from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageForm, AddressForm, Example, CustomerForm
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import *
from instamojo_wrapper import Instamojo
from django.conf import settings
from django.http import HttpResponseRedirect
from dal import autocomplete
import os

from .models import *

api = Instamojo(api_key=settings.INSTAMOJO_API_KEY,
                auth_token=settings.INSTAMOJO_API_TOKEN)


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


class CartList(LoginRequiredMixin, ListView):
    model = OrderItem
    template_name = 'cart.html'
    context_object_name = 'cart'

    def get_queryset(self):
        return OrderItem.objects.filter(customer=self.request.user.customer).filter(order=None)


@login_required
def cart_create(request, pk):
    obj = OrderItem()
    obj.item = Product.objects.get(pk=pk)
    obj.no_of_items = 0
    obj.total = 0
    obj.customer = request.user.customer
    obj.save()
    return redirect('online:cart')


class OrderDetail(LoginRequiredMixin, DetailView):
    model = Order
    template_name = ''
    context_object_name = 'orderd'


class SignUp(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('online:customercreate')

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        print(username, password)
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(SignUp, self).form_valid(form)


def sign_up(request):
    if request.method == "POST":
        sign = UserCreationForm(request.POST)
        if sign.is_valid():
            sign.save()
            u = sign.cleaned_data.get('username')
            p = sign.cleaned_data.get('password1')
            user = authenticate(username=u, password=p)
            login(request, user)
            return redirect('online:customercreate')
        else:
            return render(request, 'registration/signup.html', {'form': sign})
    else:
        sign = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': sign})


@login_required
def delete_item(request):
    pk = request.GET.get('pk')
    obj = OrderItem.objects.get(id=int(pk))
    obj.delete()
    data = {}
    return JsonResponse(data)


@login_required
def clear_cart(request):
    obj_list = OrderItem.objects.filter(order__isnull=True).filter(customer=request.user.customer)
    for i in obj_list:
        i.delete()
    return redirect('online:cart')


def get_no_items(request):
    data = {
        'number': OrderItem.objects.filter(customer=request.user.customer).filter(order=None).count()
    }
    return JsonResponse(data)


def get_total(request):
    total = 0
    for i in OrderItem.objects.filter(customer=request.user.customer).filter(order=None):
        total += i.total
    data = {
        'total': total,
    }
    print(total)
    return JsonResponse(data)


def check_cart(request):
    pk = request.GET.get('pk')
    print(pk)
    obj = get_object_or_404(Product, pk=int(pk)).orderitem_set.all().filter(customer=request.user.customer).filter(
        order=None)
    if obj.exists():
        check = 1
    else:
        check = 0
    data = {
        'check': check
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


class MessageCreate(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'contact.html'
    success_url = reverse_lazy('online:home')

    def form_valid(self, form):
        model = form.save(commit=False)
        customer = self.request.user.customer
        model.customer = customer
        model.save()
        return super(MessageCreate, self).form_valid(form)


class AddressCreate(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'checkout.html'

    def form_valid(self, form):
        model = form.save()
        order_obj = Order.objects.get(pk=self.kwargs['pk'])
        order_obj.address = model
        order_obj.save()
        return super(AddressCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('online:ordersummary', kwargs={'pk': self.object.order.pk})
        # render(self.request, 'ordersummary.html', {'order': self.object.order})


@login_required
def order_create(request):
    item_list = OrderItem.objects.filter(customer=request.user.customer).filter(order=None)
    order_obj = Order()

    order_obj.customer = request.user.customer
    # order_obj.address = Address.objects.get(pk=pk)
    sum_of_item = 0
    order_obj.save()
    for item in item_list:
        sum_of_item += item.total
        item.order = order_obj
        item.save()
    order_obj.amount = sum_of_item
    orderpk = order_obj.pk
    order_obj.save()
    return redirect('online:checkout', pk=orderpk)


def payment_request(request, pk):
    order_obj = Order.objects.get(id=pk)
    if not order_obj.address:
        return redirect('online:checkout', pk=order_obj.pk)
    else:
        response = api.payment_request_create(
            amount=10,
            purpose='Order id-{0}'.format(pk),
            send_email=True,
            buyer_name=request.user.customer.name,
            phone=str(request.user.customer.contact_no),
            send_sms=True,
            email=request.user.email,
            redirect_url=request.build_absolute_uri(reverse('online:paymentsuccess', args=(pk,)))
        )
        payment_request_id = response['payment_request']['id']
        payment_status = response['payment_request']['status']
        try:
            if order_obj.payment:
                order_obj.payment.delete()

        except:
            pass
        payment = Payment(payment_request_id=payment_request_id, payment_status=payment_status)
        payment.order = order_obj
        payment.save()
        return HttpResponseRedirect(str(response['payment_request']['longurl']))


class ProductAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Product.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class ProductSearch(FormView):
    template_name = 'example.html'
    success_url = reverse_lazy('online:home')
    form_class = Example


class CustomerCreation(CreateView):
    model = Customer
    template_name = 'registration/customer.html'
    form_class = CustomerForm
    success_url = reverse_lazy('online:home')

    def form_valid(self, form):
        model = form.save(commit=False)
        model.user_details = self.request.user
        model.save()
        return super(CustomerCreation, self).form_valid(form)


class Profile(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'


class OrderSummary(DetailView):
    model = Order
    template_name = 'ordersummary.html'
    context_object_name = 'order'


class OrderList(ListView):
    model = Order
    template_name = 'orderlist.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.customer).order_by('-date')


def payment_success(request, pk):
    payment_id = request.GET['payment_id']
    payment_status = request.GET['payment_status']
    payment_request_id = request.GET['payment_request_id']
    order = Order.objects.get(pk=pk)
    order.payment.payment_id = payment_id
    order.payment.payment_status = payment_status
    order.payment_success = True
    order.payment.save()
    order.save()
    return render(request, 'payment_success.html', {'order': order})



