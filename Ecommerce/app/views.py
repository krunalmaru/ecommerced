from django.shortcuts import render
from .models import Slider,Banner,Category,MainCategory,Subcategory
# Create your views here.
def home(request):
    slider =  Slider.objects.all().order_by('-id')[0:3]
    banner = Banner.objects.all().order_by('id')[0:3]
    maincategory = MainCategory.objects.all()
    context = {'slider':slider,'banner':banner, 'maincategory':maincategory}

    return render(request, 'home/home.html',context)