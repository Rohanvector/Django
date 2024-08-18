from django.http import JsonResponse
from django.shortcuts import redirect, render , HttpResponse
# Create your views here.
from shop.form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json

def home(request):
    products= Product.objects.filter(trending=1)
    return render(request,"shop/home.html",{"Products": products})
    

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged In Successfully ")
                return redirect("/")
            else:
                messages.error(request,"Invalid Username or Password ")
        return render(request,"shop/login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logout Successfully ")
        return redirect("/")




def reg(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success You Can Login Now..!")
            return redirect('/login') 
    return render(request,"shop/reg.html",{'form':form})


def col(request):
    catagory = Catagory.objects.filter(status = 0)
    return render(request,"shop/col.html",{"Catagory": catagory})
def colv(request,name):
    if (Catagory.objects.filter(name= name,status = 0)):
        products= Product.objects.filter(catagory__name=name)
        return render(request,"shop/products/product.html",{"Products": products,"Catagory_name": name})
    else:
        messages.warning(request,"No Such Catagary Found")
        return redirect('col')

def prod(request,cname,pname):
    if (Catagory.objects.filter(name= cname,status = 0)):
        if (Product.objects.filter(name= pname,status = 0)):
            productsd = Product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/prod.html",{"Products": productsd})
        else:
            messages.error(request,"No Such Product Found")
            return redirect('col')
    else:
        messages.error(request,"No Such Catagary Found")
        return redirect('col')
    

def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            #print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product Not Available'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart '},status=200)
    else:
        return JsonResponse({'status':'Invalid Access '},status=200)
    

def cart_page(request):
    if request.user.is_authenticated:
        Cart=cart.objects.filter(user=request.user)
        return render(request,'shop/cart.html',{'Cart':Cart})
    else:
        return redirect("/")
    
def remove_cart(request,cid):
    cartitem=cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")

def add_to_fav(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['pid']
            print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Favourite '},status=200)
                else: 
                    Favourite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'Product Added to Favourite '},status=200)
            
        else:
          return JsonResponse({'status':'Login to Favourite'},status=200)
    else:
      return JsonResponse({'status':'Invalid Access rogsn '},status=200)
    


def fav_page(request):
 if request.user.is_authenticated:
     favourite=Favourite.objects.filter(user=request.user)
     return render(request,'shop/fav.html',{'favourite':favourite})
 else:
     return redirect("/")
 
def remove_fav(request,fid):
   item=Favourite.objects.get(id=fid)
   item.delete()
   return redirect("/favourite")