from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.my_reviews, name='my_reviews'),
    path('booking/<int:booking_id>/new/', views.review_create, name='create'),
    path('favorites/', views.my_favorites, name='favorites'),
    path('favorites/<int:provider_id>/toggle/', views.favorite_toggle, name='favorite_toggle'),
]
