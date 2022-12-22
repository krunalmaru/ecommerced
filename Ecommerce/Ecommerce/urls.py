"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('404', views.error404, name='404'),
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('productdetail/<slug:slug>', views.productdetails, name="product_detail"),
    path('product', views.product,name='product'),
    path('product/filter-data',views.filter_data,name='filter-data'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('contact', views.contactus, name="contactus"),
    path('account/myaccount', views.myaccount, name='myaccount'),
    path('account/register', views.register, name='userregister'),
    path('account/login', views.loginuser, name='userlogin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('account/profile', views.PROFILE, name='profile'),
    path('account/profile/update', views.profileupdate, name='profileupdate'),
    


]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
