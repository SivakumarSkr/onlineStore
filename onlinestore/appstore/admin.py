from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Section)
admin.site.register(Attribute)
admin.site.register(Value)
admin.site.register(ProductImage)
