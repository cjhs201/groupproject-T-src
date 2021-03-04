from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserProfileForm, UserUpdateForm, ProfileUpdateForm
from .models import UserProfile, Post
from django.contrib.auth.decorators import login_required

posts = [
    {
        'author': 'admin',
        'title': '5k run',
        'description': 'Ran down to the quay',
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
        'posts': Post.objects.all() #Gets all post objects from database
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

@login_required
def editprofile(request):
    if request.method=='POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('gamma-profile')

    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.userprofile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }

    return render(request, 'gamma/editprofile.html', context)
    
