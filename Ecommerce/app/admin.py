from django.contrib import admin
from .models import Slider,Banner,Category,MainCategory,Subcategory,Product,Productimage,Section,AdditionInfo
# Register your models here.

class Productimages(admin.TabularInline):
    model = Productimage

class AdditionInfos(admin.TabularInline):
    model = AdditionInfo

class ProductAdmin(admin.ModelAdmin):
    inlines = (Productimages,AdditionInfos )

admin.site.register(Slider)
admin.site.register(Banner)
admin.site.register(MainCategory)
admin.site.register(Subcategory)
admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(Productimage)
admin.site.register(Section)
admin.site.register(AdditionInfo)



