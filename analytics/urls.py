from django.urls import path

from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.analytics_dashboard, name='dashboard'),
    path('audit-logs/', views.audit_logs, name='audit_logs'),
]
