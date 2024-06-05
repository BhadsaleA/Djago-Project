from django.shortcuts import render,redirect
from .models import *
import stripe
from datetime import datetime,timedelta
# Create your views here.

def home(request):
    course = Course.objects.all()
    context = {'coureses':course}
    return render(request,'home.html',context)

def CourseView(request,slug):
    course = Course.objects.filter(slug=slug).first()
    course_module = CourseModule.objects.filter(Course=course)
    context = {'course':course,'course_module':course_module}
    return render(request,'course.html',context)

def charge(request):
    return render(request,'harge.html')

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