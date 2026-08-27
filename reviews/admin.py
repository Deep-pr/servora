from django.contrib import admin

from .models import Favorite, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('provider', 'customer', 'overall_rating', 'created_at')
    list_filter = ('overall_rating', 'created_at')
    search_fields = ('provider__business_name', 'customer__username', 'comment')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('customer', 'provider', 'created_at')

# Register your models here.
