from django.urls import path

from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.my_bookings, name='my_bookings'),
    path('provider/<int:provider_id>/new/', views.booking_create, name='create'),
    path('<int:pk>/', views.booking_detail, name='detail'),
    path('<int:pk>/cancel/', views.booking_cancel, name='cancel'),
    path('<int:pk>/status/<str:status>/', views.provider_update_status, name='provider_update_status'),
    path('<int:booking_id>/quotes/new/', views.quote_create, name='quote_create'),
    path('quotes/<int:pk>/<str:status>/', views.quote_decision, name='quote_decision'),
]
