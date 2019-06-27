from django import forms

class BookCommentForm(forms.Form):
    text = forms.CharField(help_text="Enter your comment here.")

    def clean_renewal_date(self):
        data = self.cleaned_data['text']
        return data