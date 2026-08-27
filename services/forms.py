from django import forms

from .models import ServiceCategory


class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ('name', 'slug', 'icon', 'description', 'is_active')
