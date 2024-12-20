from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Category,Profile,Review
from django.core.paginator import Paginator

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .form import ProfileUpdateForm,ReviewForm


# Create your views here.

def index(request):
    cate=Category.objects.all()
    cateid=request.GET.get('category')
    if cateid:
            product=Product.objects.filter(subcategory=cateid)
            
    else:
        product=Product.objects.all()
        
        
    paginator=Paginator(product,2)
    num_page=request.GET.get('page')
    data=paginator.get_page(num_page) #it fetch current page data
    total=data.paginator.num_pages #3
        
    context={
        'product':product,
        'cate':cate,
        'data':data,
        'num':[i+1 for i in range(total)]#1,2,3
        }
    return render(request,'main/index.html',context)

def blog_single(request):
    return render(request,'main/blog-single.html')
def blog(request):
    return render(request,'main/blog.html')


def checkout(request):
    return render(request,'main/checkout.html')
def contact_us(request):
    return render(request,'main/contact-us.html')
def product_detail(request,id):
    product=get_object_or_404(Product,id=id)
    
    products=Product.objects.filter(category=product.category).exclude(id=id)

    cmt_all=request.GET.get('cmt_all')
    if cmt_all:
        reviews=course.reviews.all()
    else:
        reviews=course.reviews.all()[:3]
    
    form=ReviewForm()
    if request.method=='POST':
        form=ReviewForm(request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.user=request.user
            review.course=course
            review.save()
            return redirect('product_detail',id=id)
    
    context={
        'product':product,
        'products':products,
        'form':form,
        'reviews':reviews,
        'range':range(1,6),
        'cmt_all':cmt_all
    }
    
    return render(request,'main/product-details.html',context)
def shop(request):
    return render(request,'main/shop.html')


def log_in(request):
    return render(request,'auth/login.html')

def register(request):
    # data=Register.objects.all()
    if request.method=='POST':
        first_name = request.POST['first_name']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        confirm_password=request.POST['password1']

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request,"username is already exist")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email already exist")
                return redirect("register")
            else:
                User.objects.create_user(first_name=first_name,email=email,username=username,password=password)
                return redirect('log_in')
        else:

          messages.error(request,"password and confirm password is not match!")
        return redirect("register")
    


    return render(request,'auth/register.html')

def log_in(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(username=username,password=password)
        if not User.objects.filter(username=username).exists():
            messages.info(request,"userename is not found")

        if user is not None:
            login(request,user)
            return redirect('index')
        

    return render(request,'auth/login.html')
def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url='log_in')
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')    
    return render(request,'auth/change_password.html',{'form':form})

@login_required(login_url='log_in')
def customer_profile(request):
    profile,created=Profile.objects.get_or_create(user=request.user)
    profile_form=ProfileUpdateForm(instance=profile)
    
    if request.method=='POST':
        profile_form=ProfileUpdateForm(request.POST,request.FILES,instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
        
    context={
        'form':profile_form,
        'user':request.user,
        'profile':request.user.profile
    }
    return render(request,'main/customer_profile.html',context)


from django.contrib.auth.decorators import login_required
from cart.cart import Cart


@login_required(login_url="log_in")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="log_in")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart")


@login_required(login_url="log_in")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart")


@login_required(login_url="log_in")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart")


@login_required(login_url="log_in")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart")


@login_required(login_url="log_in")
def cart_detail(request):
    return render(request, 'main/cart.html')