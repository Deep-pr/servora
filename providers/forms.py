from django import forms

from .models import ProviderService, VerificationDocument


class ProviderServiceForm(forms.ModelForm):
    class Meta:
        model = ProviderService
        fields = ('category', 'title', 'description', 'starting_price', 'is_active')


class VerificationDocumentForm(forms.ModelForm):
    class Meta:
        model = VerificationDocument
        fields = ('document_type', 'document')

    def clean_document(self):
        document = self.cleaned_data['document']
        max_size = 5 * 1024 * 1024
        allowed_extensions = ('.pdf', '.jpg', '.jpeg', '.png')
        if document.size > max_size:
            raise forms.ValidationError('Document must be 5 MB or smaller.')
        if not document.name.lower().endswith(allowed_extensions):
            raise forms.ValidationError('Only PDF, JPG, JPEG, and PNG files are allowed.')
        return document
