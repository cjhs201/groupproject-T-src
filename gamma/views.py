from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Avg
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserProfileForm, UserUpdateForm, ProfileUpdateForm, CommentForm, RatePostForm
from .models import UserProfile, Post, Comment, PostRating
from django.contrib.auth.decorators import login_required


# terms and conditions
def tc(request):
    return render(request, 'gamma/tc.html')

def index(request):
    context = {
        'posts': Post.objects.all() #Gets all post objects from database
    }
    return render(request, 'gamma/index.html', context)

#The method that is called when you need to register. It takes a value request and returns the user to login page
#if created
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
def profile(request): #This is the user's locally viewed profile
    context = {
        'posts': Post.objects.all()  # Makes all posts available to the profile page so that a user's activities can be displayed on their profile
    }
    return render(request, 'gamma/profile.html', context)

class UserProfileView(DetailView): #This is a profile that can be viewed by anyone
    model = UserProfile
    template_name = 'gamma/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()  # show all a user's activities on their profile page
        return context

# method called when a user wants to edit their profile
# will update both the profile and user details
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

class PostListView(ListView):
    model = Post
    template_name = 'gamma/index.html'
    context_object_name = 'posts'
    ordering = ['-date_posted'] #-date_posted sorts posts from newest to oldest instead of oldest to newest
    paginate_by = 4 # Sorts by 4 posts per page


#The view for the Posts showing how they are edited
class PostDetailView(DetailView):
    model = Post
    template_name = 'gamma/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['rating_form'] = RatePostForm()
        context['comments'] = Comment.objects.filter(post=self.get_object()).order_by("-date_posted")
        return context

    
    def post(self, req, *args, **kwargs):
        currentpost = self.get_object()
        post_author_profile = currentpost.author.userprofile
        if "submit-comment" in req.POST: # for posting a comment to a post
            form = CommentForm(req.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = req.user
                comment.post = currentpost
                comment.is_rating = False
                comment.save()
        elif "submit-rating" in req.POST:
            form = RatePostForm(req.POST)
            if Comment.objects.filter(author=req.user, post=currentpost, is_rating=True).first(): #only allows to rate each post once
                messages.error(req, "You have already rated this post.")
            elif form.is_valid():
                rating = form.save(commit=False)
                rating.author = req.user
                rating.post = currentpost
                rating.save()
                currentpost.rating = PostRating.objects.filter(post=self.get_object()).aggregate(Avg('rating'))['rating__avg']
                currentpost.save()
                post_author_profile.points += rating.rating # adds rating to points of user that created the post
                post_author_profile.save()
                comment = Comment(is_rating=True, content=f"{rating.rating}", author=req.user, post=currentpost)
                comment.save()
        return HttpResponseRedirect(f"/post/{currentpost.id}")

class PostCreateView(LoginRequiredMixin, CreateView): #LoginRequiredMixin ensures that a user has to be logged in to create a post
    model = Post
    fields = ['title', 'type', 'description', 'distance', 'measurement', 'time', 'header_image']

    def form_valid(self, form):
        form.instance.author = self.request.user #Will automatically set the author of the post to the user who is currently logged in
        return super().form_valid(form) #This would normally be passed anyway but is overwritten by us

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #UserPassesTestMixin is used to check if user updating a post is the owner of that post
    fields = ['title', 'type', 'description', 'distance', 'measurement', 'time', 'rating', 'header_image']
    model = Post
    success_url = '/' #sends user to homepage after deletion

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_updae(self, form, User):
        User.points += form.points # adds the points to the user's points
        return super().form_valid(form)

    def test_func(self): # tests if user is owner of post
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): #LoginRequiredMixin ensures that a user has to be logged in to delete a post
    model = Post
    success_url = '/' #sends user to homepage after deletion

    def test_func(self): #tests if user is owner of post
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class LeaderboardListView(ListView):
    model = UserProfile
    template_name = 'gamma/leaderboards.html'
    context_object_name = 'users'
    ordering = ['-points'] #-date_posted sorts posts from newest to oldest instead of oldest to newest