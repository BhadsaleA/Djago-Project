from django.shortcuts import render,redirect
from .models import *
import stripe
from datetime import datetime,timedelta
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    course = Course.objects.all()
    context = {'coureses':course}

    # if request.user.is_authenticated:
        # profile = Profile.objects.filter(user = request.user).first()
        # request.session['profile'] = profile.is_pro
        # return render(request,'home.html',context)
    return render(request,'home.html',context)


def CourseView(request,slug):
    course = Course.objects.filter(slug=slug).first()
    course_module = CourseModule.objects.filter(Course=course)
    context = {'course':course,'course_module':course_module}
    return render(request,'course.html',context)

def charge(request):
    return render(request,'harge.html')

def Login(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username is None:
            context = {'message':'User does not register'}
            return render(request,'register.html')
        else:
            user = authenticate(username=username,password=password)
            if user is None:
                context = {'message':'wrong password'}
                return render(request,'login.html')
            else:
                login(request,user)
                return redirect('/')
    
    return render(request,'login.html')

def Logout(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user :
            context = {'message':'User already registered'}
            return render(request,'register.html',context)
        else:
            user =User(username=username,email=email)
            user.set_password(password)
            user.save()
            context = {'message':'User registered..!'}
            return render(request,'register.html')
    return render(request,'register.html')

def become_pro(request):
    if request.method =='POST':
        membership = request.POST.get('membership','MONTHLY')
        amount = 1000
        if membership == 'YEARLY':
            amount = 11000
        stripe.api_key = "sk_test_tR3PYbcVNZZ796tH88S4VQ2u"

        customer = stripe.Customer.create(
            email= request.user.email,
            source= request.POST['stripeToken']
        )
        charge = stripe.Charge.create(
            customer= customer,
            amount= amount *100,
            currency= 'inr',
            description= 'membership'
        )

        if charge['paid'] == True:
            profile = Profile.objects.filter(user=request.user).first()
            if charge['amount'] == 100000:
                profile.subscription_type = 'M'
                profile.is_pro = True
                expiry = datetime.now() + timedelta(30)
                profile.pro_exipry_date = expiry
                profile.save()
            elif charge['amount'] == 1100000:
                profile.subscription_type = 'Y'
                profile.is_pro = True
                expiry = datetime.now() + timedelta(365)
                profile.pro_exipry_date = expiry
                profile.save()  

        return redirect('/charge/')
    return render(request,'become_pro.html')