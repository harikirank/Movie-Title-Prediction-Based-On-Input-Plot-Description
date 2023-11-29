from django import forms
from django.core.exceptions import ValidationError


class TitlePredictionForm(forms.Form):
    plot = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter the plot of the movie here...'}))

    def clean_plot(self):
        new_plot = self.cleaned_data['plot']
        if len(new_plot) == 0:
            raise ValidationError("Plot can't be empty.")