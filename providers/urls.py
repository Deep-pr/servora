from django.urls import path

from . import views

app_name = 'providers'

urlpatterns = [
    path('me/services/', views.my_services, name='my_services'),
    path('me/services/add/', views.service_create, name='service_create'),
    path('me/services/<int:pk>/edit/', views.service_update, name='service_update'),
    path('me/services/<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('me/verification/', views.verification, name='verification'),
    path('', views.provider_search, name='search'),
    path('<int:pk>/', views.provider_profile, name='profile'),
]
