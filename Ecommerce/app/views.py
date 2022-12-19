from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
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

def myaccount(request):

    return render(request, 'accounts/myaccounts.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User(username=username, email=email)
        user.set_password(password)
        print(user)
        user.save()
        return redirect('myaccount')

def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect('myaccount')

    return render(request, 'accounts/myaccounts.html')