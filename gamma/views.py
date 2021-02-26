from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserProfileForm

def index(request):
    return render(request, 'gamma/index.html')

def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'You have successfully registered as {username}!')
    else:
        form = UserRegisterForm()
        profile_form = UserProfileForm()
    return render(request, 'gamma/register.html', {'form': form, 'profile_form': profile_form})

'''def login(request):
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
    return render(request, 'gamma/user_profile.html',)'''
    
    