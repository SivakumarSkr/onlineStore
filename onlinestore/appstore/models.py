import datetime
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django_resized import ResizedImageField


# Create your models here.
class Address(models.Model):
    def pincode_validators(x):
        if len(str(x)) != 6:
            raise ValidationError('Invalid Pincode')
    name = models.CharField('Name', max_length=30, null=True)
    email = models.EmailField('Email', null=True)
    phone = PhoneNumberField(null=True)
    address = models.TextField('Address', max_length=500, null=True)
    city = models.CharField('City', max_length=50)
    district = models.CharField('District', max_length=20)
    pin_code = models.PositiveIntegerField('Pincode', validators=[pincode_validators])


class Customer(models.Model):
    user_details = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=50)
    contact_no = PhoneNumberField()
    # address = models.OneToOneField(Address, on_delete=models.CASCADE)
    profile_pic = models.ImageField('Profile Picture', upload_to='profile/', default='profile/default.jpg')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Name', max_length=20)
    image = ResizedImageField(upload_to='{}/'.format('Category'), default='category/default.jpg')
    descrip = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=35)
    descrip = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_code = models.CharField('Produce code', max_length=20)
    name = models.CharField("Name", max_length=50)
    price = models.PositiveIntegerField()
    in_stock = models.BooleanField(default=True)
    caption = models.CharField('Caption', max_length=100)
    number_of_stock = models.PositiveIntegerField()
    # description = models.TextField('About', max_length=500, null=True)
    category = models.ForeignKey(SubCategory, verbose_name='Sub category', on_delete=models.CASCADE)
    image = ResizedImageField(size=[800, 800], upload_to='{}/'.format('image'), default='image/default.jpg')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('product', args=[str(self.pk)])

# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
#     image = models.ImageField('Image', upload_to='{}/'.format('image'), default='image/default.jpg')
#
#     def __str__(self):
#         return str(self.pk)


class Description(models.Model):
    name = models.CharField("Spec", max_length=50)
    Product = models.ManyToManyField(Product, verbose_name='Product')

    def __str__(self):
        return self.name


class Order(models.Model):
    code = models.UUIDField('Order ID', default=uuid.uuid1)
    date = models.DateTimeField('Date of order', default=datetime.datetime.now)
    customer = models.ForeignKey(Customer, verbose_name='Customer', on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.PROTECT, null=True)
    amount = models.PositiveIntegerField('Amount', default=0)
    payment_success = models.BooleanField(default=False)


class OrderItem(models.Model):
    item = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Customer')
    no_of_items = models.PositiveIntegerField()
    order = models.ForeignKey(Order, verbose_name='order', on_delete=models.CASCADE, null=True)
    total = models.PositiveIntegerField()

    def __str__(self):
        return self.item.name


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(default=datetime.datetime.now)
    payment_request_id = models.CharField(max_length=25)
    payment_id = models.CharField(max_length=25, null=True)
    payment_status = models.CharField(max_length=20)


class Message(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='User', null=True)
    name = models.CharField('Name', max_length=50)
    subject = models.CharField('Subject', max_length=200)
    message = models.TextField('Message', max_length=1000)

    def __str__(self):
        return self.subject

