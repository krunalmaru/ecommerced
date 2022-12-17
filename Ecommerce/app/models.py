from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
class Slider(models.Model):
    Discount_Deal = (
        ('HOT DEALS','HOT DEALS'),
        ('New DEALS','New DEALS')
    )
    image = models.ImageField(upload_to='media/slider_image')
    discount_deal = models.CharField(choices=Discount_Deal, max_length=100)
    brand_name = models.CharField(max_length=200)
    sale = models.IntegerField()
    discount = models.IntegerField()
    link = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.brand_name

class Banner(models.Model):
    image = models.ImageField(upload_to='media/banner_img')
    discount_deal = models.CharField(max_length=100)
    quote = models.CharField(max_length=100, null=True,blank=True)
    discount = models.IntegerField()
    link = models.CharField(max_length=100,null=True)

    def __str__(self) -> str:
        return self.quote

class MainCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Category(models.Model):
    maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name + "--" + self.maincategory.name
    
class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.category.maincategory.name + "--" + self.category.name + "--" + self.name

class Section(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    total_quantity = models.IntegerField()
    availability = models.IntegerField()
    feature_image = models.CharField(max_length=100)
    price = models.IntegerField()
    discount = models.IntegerField()
    product_information = RichTextField()
    model_name = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)
    description = RichTextField()
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.product_name

class Productimage(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    imageurl = models.CharField(max_length=150)

class AdditionInfo(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    specification = models.CharField(max_length=255)
    detail = models.CharField(max_length=255)
