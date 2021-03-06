from django.contrib import admin
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserProfileView, LeaderboardListView
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #These are the urls for the websites
    path('admin/', admin.site.urls),
    path('', PostListView.as_view(), name="index"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"), #this is the URL created from a specific post pk=primary key
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="post-delete"),
    path('register/', views.register, name="gamma-register"),
    path('register/tc', views.tc, name="gamma-register-tc"),
    path('login/', auth_views.LoginView.as_view(template_name='gamma/login.html'), name="gamma-login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='gamma/logout.html'), name="gamma-logout"),
    path('profile/', views.profile, name="gamma-profile"),
    path('profile/<int:pk>/', UserProfileView.as_view(), name="user-profile"),
    path('editprofile/', views.editprofile, name="gamma-editprofile"),
    path('leaderboard/', LeaderboardListView.as_view(), name="gamma-leaderboard"),
    
]

if (settings.DEBUG):
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
