from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserProfileForm
from .models import UserProfile, Post
from django.contrib.auth.decorators import login_required

posts = [
    {
        'author': 'admin',
        'title': '5k run',
        'description': 'Leg still not working',
        'date_posted': 'March 2nd, 2021',
        'type': 'Run',
        'distance': 5,
        'measurement': 'km',
        'rating': 4,
    },
{
        'author': 'admin',
        'title': '30k Cycle',
        'description': 'To exmouth',
        'date_posted': 'March 3rd, 2021',
        'type': 'hiit',
        'distance': 30,
        'measurement': 'km',
        'rating': 8,
    }
]

def index(request):
    context = {
        'posts': posts #Post.objects.all()
    }
    return render(request, 'gamma/index.html', context)

def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, f'Your account has been created. Please log in.')
            return redirect('gamma-login')
    else:
        form = UserRegisterForm()
        profile_form = UserProfileForm()
    return render(request, 'gamma/register.html', {'form': form, 'profile_form': profile_form})

@login_required
def profile(request):
    return render(request, 'gamma/profile.html')
    
    