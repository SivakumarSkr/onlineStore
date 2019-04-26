# Generated by Django 2.1.5 on 2019-04-18 17:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('appstore', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='code',
            field=models.UUIDField(default=uuid.uuid1, verbose_name='Order ID'),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
