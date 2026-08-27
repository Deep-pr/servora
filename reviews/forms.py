from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = (
            'overall_rating',
            'service_quality',
            'professionalism',
            'punctuality',
            'pricing',
            'comment',
        )
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
