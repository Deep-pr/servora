"""Servora URL configuration."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from dashboard import views as public_views

urlpatterns = [
    path('', public_views.home, name='home'),
    path('about/', public_views.about, name='about'),
    path('contact/', public_views.contact, name='contact'),
    path('faq/', public_views.faq, name='faq'),
    path('dashboard/', include('dashboard.urls')),
    path('services/', include('services.urls')),
    path('providers/', include('providers.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
