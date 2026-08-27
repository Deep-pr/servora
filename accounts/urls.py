from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('register/customer/', views.customer_register, name='customer_register'),
    path('register/provider/', views.provider_register, name='provider_register'),
    path('profile/', views.profile, name='profile'),
]
