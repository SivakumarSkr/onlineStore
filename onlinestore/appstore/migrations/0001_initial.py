# Generated by Django 2.1.7 on 2019-03-16 07:39

import appstore.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house_or_flat', models.CharField(max_length=50, verbose_name='House name /Flat no')),
                ('post', models.CharField(max_length=50, verbose_name='Post office')),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('district', models.CharField(max_length=20, verbose_name='District')),
                ('pincode', models.PositiveIntegerField(validators=[appstore.models.Address.pincode_validators], verbose_name='Pincode')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Name')),
                ('image', models.ImageField(default='category/default.jpg', upload_to='Category/')),
                ('descrip', models.TextField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('contact_no', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('profile_pic', models.ImageField(default='profile/default.jpg', upload_to='profile/', verbose_name='Profile Picture')),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='appstore.Address')),
                ('user_details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Spec')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.UUIDField(default=uuid.uuid1, verbose_name='Order ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Date of order')),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='appstore.Address')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appstore.Customer', verbose_name='Customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_items', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_code', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Produce code')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('price', models.PositiveIntegerField()),
                ('in_stock', models.BooleanField(default=True)),
                ('caption', models.CharField(max_length=100, verbose_name='Caption')),
                ('number_of_stock', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='image/default.jpg', upload_to='image/', verbose_name='Image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appstore.Product', verbose_name='Product')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Name')),
                ('image', models.ImageField(default='subcategory/default.jpg', upload_to='Subcategory/')),
                ('descrip', models.TextField(max_length=1000)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appstore.Category', verbose_name='Category')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appstore.SubCategory', verbose_name='Sub category'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appstore.Product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='description',
            name='Product',
            field=models.ManyToManyField(to='appstore.Product', verbose_name='Product'),
        ),
    ]