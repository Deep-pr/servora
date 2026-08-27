from django import forms

from .models import Booking, Quote


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('provider_service', 'scheduled_for', 'address', 'problem_description', 'contact_preference')
        widgets = {
            'scheduled_for': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'problem_description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, provider=None, **kwargs):
        super().__init__(*args, **kwargs)
        if provider:
            self.fields['provider_service'].queryset = provider.services.filter(is_active=True).select_related('category')


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ('estimated_price', 'service_description', 'expected_completion_time', 'notes', 'expires_at')
        widgets = {
            'service_description': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
