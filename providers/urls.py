from django.urls import path

from . import views

app_name = 'providers'

urlpatterns = [
    path('', views.provider_search, name='search'),
    path('<int:pk>/', views.provider_profile, name='profile'),
]
