from django import forms
from django.forms import ModelForm

from products.models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = (
            "message",
            "mark",
            "is_anonymous"
        )

    message = forms.CharField(required=False)
    mark = forms.FloatField()
    is_anonymous = forms.BooleanField(required=False, initial=False)
