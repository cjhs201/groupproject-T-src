from django.shortcuts import render
from gamma.models import UserDetails
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm

def index(request):
    return render(request, 'gamma/index.html')

def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'You have successfully registered as {username} !')
    else:
        form = UserRegisterForm()
    return render(request, 'gamma/register.html', {'form': form})

def login(request):
    if request.method=="POST":
        try:
            Details=UserDetails.objects.get(email=request.POST['email'], password=request.POST['password'])
            print("email=", Details)
            request.session['email']=Details.email
            return render(request, 'index.html')
        except UserDetails.DoesNotExist as e:
            messages.success(request, 'Email / Password Invalid..!')
    return render(request, 'gamma/login.html')

def logout(request):
    try:
        del request.session['email']
    except:
        return render(request,'index.html')
    return render(request,'index.html')

def user_profile(request):
    return render(request, 'gamma/user_profile.html',)
    
    