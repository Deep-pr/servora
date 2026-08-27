from django.urls import path

from . import views

app_name = 'services'

urlpatterns = [
    path('manage/', views.category_manage, name='category_manage'),
    path('manage/add/', views.category_create, name='category_create'),
    path('manage/<int:pk>/edit/', views.category_update, name='category_update'),
    path('manage/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('', views.service_list, name='list'),
    path('<slug:slug>/', views.service_detail, name='detail'),
]
