from django.contrib import admin
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserProfileView
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PostListView.as_view(), name="index"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"), #this is the URL created from a specific post pk=primary key
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="post-delete"),
    path('register/', views.register, name="gamma-register"),
    path('login/', auth_views.LoginView.as_view(template_name='gamma/login.html'), name="gamma-login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='gamma/logout.html'), name="gamma-logout"),
    path('profile/', views.profile, name="gamma-profile"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='gamma/password_reset.html'), name="gamma-password_reset"),
    path('profile/<int:pk>/', UserProfileView.as_view(), name="user-profile"),
    path('editprofile/', views.editprofile, name="gamma-editprofile"),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='gamma/password_reset_done.html'), name="gamma-password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='gamma/password_reset_confirm.html'), name="gamma-password_reset_confirm"),
]

if (settings.DEBUG):
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
