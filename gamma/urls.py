from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('register/', views.register, name="gamma-register"),
    path('login/', auth_views.LoginView.as_view(template_name='gamma/login.html'), name="gamma-login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='gamma/logout.html'), name="gamma-logout"),
    path('profile/', views.profile, name="gamma-profile"),
    path('editprofile/', views.editprofile, name="gamma-editprofile"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
