from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import Q

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.decorators import api_view
from rest_framework.response import Response

from LIFE import settings
from Slife.forms import RegisterForm, LoginForm, CommentForm, ContactForm
from Slife.models import Category, Option, Vote
from Slife.serializers import CategorySerializer, OptionSerializer
#from Slife.tokens import activation_token
# Create your views here.



def home(request):
    categories = Category.objects.filter(active=True,views__gte=3000).order_by('-views')
    featured_categories = Category.objects.filter(active=True,featured=True)
    return render(request,'Slife/base.html',{'categories': categories,'featured_categories':featured_categories,'title':'LIFE'})


def all_categories(request):
    categories = Category.objects.filter(active=True)
    return render(request,'Slife/categories.html',{'categories':categories,'title':'LIFE'})


def search(request):
    q = request.GET['q']
    if q:
        categories = Category.objects.filter(name__icontains=q)
        return render(request,'Slife/categories.html',{'categories':categories})
    else:
        return redirect('/')


def options(request,slug):
    category = Category.objects.get(slug=slug)        
    category.views += 1
    category.save()
    options = category.option_set.all().order_by('-votes')
    try:
        for option in options:
            option.has_voted = option.vote_set.filter(voter=request.user).exists()
    except:
        options = category.option_set.all().order_by('-votes')

    form = CommentForm()
    return render(request, 'Slife/options.html', {'options':options,'form':form,'title':'options','category':category})    


def comment(request,slug):
    if not request.user.is_authenticated:
        messages.info(request, 'You have to be logged in to post comments')
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        if request.method =="POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.category = Category.objects.get(slug=slug)
                comment.user = request.user
                comment.save()
                messages.success(request, ' Comment Posted')
        else:
             return redirect('Slife:options',slug)


def vote(request,slug):
    #if user hasnt logged in before voting 
    if not request.user.is_authenticated:
         messages.info(request,'You have to be logged in to vote.')
         return redirect('%s?next=%s' %(settings.LOGIN_URL, request.path))
    option = Option.objects.get(slug=slug)
    category = option.category

    if Vote.objects.filter(slug=slug, voter_id=request.user.id).exists():
         messages.error(request, 'Sorry! You Already Voted')
         return redirect('Slife:options',category.slug)
    
    else:
         option.votes += 1
         option.save()
         voter = Vote(voter=request.user, option=option)
         #i commented the voter.save because it kep giving object attribute when you cast vote
         voter.save()
         messages.success(request, 'Voted.{} Thanks for your vote.Kindly logout now.'.format(option.votes - 1))
         return redirect('Slife:options', category.slug)

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            site = get_current_site(request)
            mail_subject = "Confirmation message"
            message = render_to_string('Slife/activate_mail.html',{
                "user":user,
                'domain':site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                #'token': activation_token.make_token(user)

            })
            to_email = form.cleaned_data.get('email')
            to_list = [to_email]
            from_email = settings.EMAIL_HOST_USER
            send_mail(mail_subject,message, from_email, to_list, fail_silently=True)
            messages.success(request,"Thanks for your registration. A confirmation link has been sent to your email")
    else :
        form = RegisterForm()
    return render(request,'Slife/register.html',{'form':form})    


def my_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = form['username'].value()
        password = form['password'].value()
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            redirect_url = request.GET.get('next','Slife:home')
            return redirect(redirect_url)
        else:
             messages.error(request,'Invalid Username or Password')
    else:
        form = LoginForm()
        return render(request,'Slife/login.html',{'form':form})    

def my_logout(request):
    logout(request)
    messages.success(request,'Logged out successfully')
    return redirect('Slife:login')            

       
   
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            messages.success(request,'Your message has been sent')
            return redirect('Slife:contact')
        else:
            messages.error(request,'Error in form.Try Again')
            return redirect('Slife:contact')
    else:
            form = ContactForm()
    return render(request, "Slife/contact.html",{'form':form})    


def about(request):
    return render(request,'Slife/about.html')


@api_view(['GET'])
def api_categories(request):
    query = request.GET.get('q','')
    categories = Category.objects.filter(Q(name__icontains=query)|Q(details__icontains=query))
    serializer = CategorySerializer(categories,many=True)
    return Response(serializer.data)

@api_view(['GET'])    
def api_options(request):
    query = request.GET.get('q','')
    options = Option.objects.filter(name__icontains=query)
    serializer = OptionSerializer(options,many=True)
    return Response(serializer.data)



# class Meta:
#         permssions = (
#             ("view vote","can vote only once"),
#             ("view vote","can vote more than once"),
#         )

        #  messages.success(request, "Voted !!".format(option.votes - 1))
        #  voter.save()
        #  return redirect('Slife:options',category.slug)
        #  messages.success(request,"Voted !!")


