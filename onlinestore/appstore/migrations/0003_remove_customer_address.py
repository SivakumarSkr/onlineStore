# Generated by Django 2.1.5 on 2019-04-12 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appstore', '0002_remove_order_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='address',
        ),
    ]