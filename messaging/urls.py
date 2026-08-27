from django.urls import path

from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.conversation_list, name='list'),
    path('start/provider/<int:provider_id>/', views.conversation_start, name='start_provider'),
    path('<int:pk>/', views.conversation_detail, name='detail'),
]
