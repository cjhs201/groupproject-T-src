from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('register/', views.register, name="gamma-register"),
    path('login/', auth_views.LoginView.as_view(template_name='gamma/login.html'), name="gamma-login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='gamma/logout.html'), name="gamma-logout"),
    path('profile/', views.profile, name="gamma-profile"),
]
