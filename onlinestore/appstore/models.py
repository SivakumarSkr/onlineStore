from django.db import models


# Create your models here.
class Section(models.Model):
    name = models.CharField("Name", max_length=20)
    image = models.ImageField("Image", upload_to='{}/'.format('Section'))
    descrip = models.TextField('Description', max_length=1000)

    def __str__(self):
        return self.name


class Category(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=20)
    image = models.ImageField(upload_to='{}/'.format('Category'), default='category/default.jpg')
    descrip = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=20)
    image = models.ImageField(upload_to='{}/'.format('Subcategory'), default='subcategory/default'
                                                                             '.jpg')
    descrip = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Name", max_length=30)
    price = models.PositiveIntegerField()
    in_stock = models.BooleanField(default=True)
    caption = models.CharField('Caption', max_length=100)
    number_of_stock = models.PositiveIntegerField()
    description = models.TextField('About', max_length=500, null=True)
    category = models.ForeignKey(SubCategory, verbose_name='Sub category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    image = models.ImageField('Image', upload_to='{}/'.format('image'), default='image/default.jpg')

    def __str__(self):
        return str(self.pk)


class Attribute(models.Model):
    name = models.CharField("Spec", max_length=20)
    description = models.TextField('Description', max_length=1000)
    Product = models.ManyToManyField(Product, verbose_name='Product')

    def __str__(self):
        return self.name


class Value(models.Model):
    name = models.CharField('Value', max_length=20)
    description = models.TextField('Description', max_length=500)
    attribute = models.ManyToManyField(Attribute, verbose_name='Attribute')

    def __str__(self):
        return self.name
