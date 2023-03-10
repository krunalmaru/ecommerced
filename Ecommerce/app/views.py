from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .models import Slider,Banner,Category,MainCategory,Subcategory,Product,Color,Brand,Coupon_code
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.db.models import Min,Max,Sum
from cart.cart import Cart


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
    colo = Color.objects.all()
    brand = Brand.objects.all()

    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))

    FilterPrice = request.GET.get('FilterPrice')
    colorID = request.GET.get('colorID')

    if FilterPrice:
        newfilterprice = int(FilterPrice)
        product = Product.objects.filter(price__lte=newfilterprice)

    elif colorID:
        product = Product.objects.filter(color = colorID)
        
    else:
        product = Product.objects.all()
    context = {'category':category, 'product':product, 'minprice':min_price,'maxprice':max_price,'FilterPrice':FilterPrice, 'colo':colo,'brand':brand}
    return render(request, 'product/product.html', context)

def filter_data(request):
    categories = request.GET.getlist('category[]')
    print(categories)
    # brands = request.GET.getlist('brand[]')
    product_num = request.GET.getlist('product_num[]')
    brand = request.GET.getlist('brand[]')
    
    allProducts = Product.objects.all().order_by('-id').distinct()
    print(allProducts)
    if len(categories) > 0:
        allProducts = allProducts.filter(categories__id__in=categories).distinct()

    if len(brand) > 0:
        allProducts = allProducts.filter(brand__id__in=brand).distinct()
    
    if len(product_num):
        allProducts = allProducts.all().order_by('-id')[0:1]
    
    if len(brand) > 0:
        allProducts = allProducts.filter(brand__id__in=brand).distinct()
    
   

    t = render_to_string('ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})


@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    cart = request.session.get('cart')
    packing_cost= sum(i['packing_cost'] for i in cart.values() if i)
    tax =sum(i['tax'] for i in cart.values() if i)
    
    coupon = None
    valid_coupon = None
    invalid_coupon = None
    if request.method == 'GET':

        coupon_code = request.GET.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon_code.objects.get(code = coupon_code)
                valid_coupon = "Are Apply on Current Order"
            except:
                invalid_coupon = "Invalid Coupon Code"
        else:
            pass

    context = {
        'packing_cost':packing_cost,
        'tax':tax,
        'coupon': coupon,
        'valid_coupon':valid_coupon,
        'invalid_coupon':invalid_coupon

        }
    return render(request, 'cart/cart.html',context)

def checkout(request):
    coupon_discount = None
    if request.method == 'POST':
        coupon_discount = request.POST.get('coupon_discount')
        if coupon_discount:
            try:
                coupon_discount = Coupon_code.objects.get(code = coupon_discount)
                valid_coupon = "Are Apply on Current Order"
            except:
                invalid_coupon = "Invalid Coupon Code"
        else:
            pass
    cart = request.session.get('cart')
    print(cart)
    packing_cost= sum(i['packing_cost'] for i in cart.values() if i)
    tax =sum(i['tax'] for i in cart.values() if i)
    tax_and_packing_cost = (tax + packing_cost)
    context = {
        'tax_and_packing_cost':tax_and_packing_cost,
        'coupon_discount':coupon_discount
    }
    return render(request,'home/checkout.html',context)
