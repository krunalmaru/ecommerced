from django.db import models

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