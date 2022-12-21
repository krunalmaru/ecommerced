from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .models import Slider,Banner,Category,MainCategory,Subcategory,Product
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string


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
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username Already Exist')
            return redirect('myaccount')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email Already Exist')
            return redirect('myaccount')
            
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        return redirect('login')

def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username and Password are Invalid')
            return redirect('login')

    # return render(request, 'accounts/myaccounts.html')

@login_required(login_url='/accounts/login/')
def PROFILE(request):
    return render(request, 'profile/profile.html')


@login_required(login_url='/accounts/login/')
def profileupdate(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, 'Your Profile Update successfully')
        return redirect('profile')
    
def aboutus(request):
    return render(request, 'home/aboutus.html')

def contactus(request):
    return render(request, 'home/contactus.html')

def product(request):
    category = Category.objects.all()
    product = Product.objects.all().order_by('-id')
    context = {'category':category, 'product':product}
    return render(request, 'product/product.html', context)

def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    print(categories)
    allProducts = Product.objects.all().order_by('-id').distinct()
    print(allProducts)
    if len(categories) > 0:
        allProducts = allProducts.filter(category__id__in=categories).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()

    t = render_to_string('ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})