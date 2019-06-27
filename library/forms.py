from django import forms

class BookCommentForm(forms.Form):
    text = forms.CharField(help_text="Enter your comment here.")

    def clean_renewal_date(self):
        data = self.cleaned_data['text']
        return data

class BookSuggestForm(forms.Form):
    title = forms.CharField(max_length=200, help_text='Enter the title of the book')
    author = forms.CharField(max_length=200, help_text='Enter the name of the author of the book')
    url = forms.URLField(max_length=200, help_text='Enter the URL of the book')
    description = forms.CharField(max_length=1000, help_text='Enter a brief description of the book')

    def clean_renewal_date(self):
        data = self.cleaned_data['title', 'author', 'url', 'description']
        return data