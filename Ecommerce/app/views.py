from django.shortcuts import render,redirect

from .models import Slider,Banner,Category,MainCategory,Subcategory,Product
# Create your views here.
def home(request):
    slider =  Slider.objects.all().order_by('-id')[0:3]
    banner = Banner.objects.all().order_by('id')[0:3]
    maincategory = MainCategory.objects.all()
    product = Product.objects.filter(section__name = 'Top Selling Products')
    context = {'slider':slider,'banner':banner, 'maincategory':maincategory,'product':product}

    return render(request, 'home/home.html',context)

def productdetails(request, slug):
    product = Product.objects.filter(slug=slug)
    if product.exists():
        product = Product.objects.get(slug = slug)
    else:
        return redirect('404')
    context = {'product':product}
    return render(request, 'product/productdetail.html', context)

def error404(request):
    return render(request, 'error/404.html')