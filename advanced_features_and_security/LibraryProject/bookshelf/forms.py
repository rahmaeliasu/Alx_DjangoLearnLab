from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "published_year"]

class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False)

    def clean_q(self):
        q = self.cleaned_data.get("q", "")
        return q.strip()
