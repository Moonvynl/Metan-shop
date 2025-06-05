from django import forms
from .models import Review

class ReviewCreateForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.RadioSelect 
    )

    class Meta:
        model = Review
        fields = ('text', 'rating')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
        }