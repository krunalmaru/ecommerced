from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User

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



class Color(models.Model):
    code = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.code

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True)
    total_quantity = models.IntegerField()
    availability = models.IntegerField()
    feature_image = models.CharField(max_length=100)
    price = models.IntegerField()
    discount = models.IntegerField()
    tax = models.IntegerField(null=True)
    packing_cost = models.IntegerField(null=True)
    product_information = RichTextField()
    model_name = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)
    description = RichTextField()
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    slug  = models.SlugField(default='', max_length=500, null=True,blank=True)

    def __str__(self) -> str:
        return self.product_name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug':self.slug})
    
    class Meta:
        db_table = "app_product"

def create_slug(instance, new_slug =None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs =Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug,qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
pre_save.connect(pre_save_post_receiver, Product)

class Coupon_code(models.Model):
    code = models.CharField(max_length=100)
    discount = models.IntegerField()

    def __str__(self) -> str:
        return self.code


class Productimage(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    imageurl = models.CharField(max_length=150)

class AdditionInfo(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    specification = models.CharField(max_length=255)
    detail = models.CharField(max_length=255)

