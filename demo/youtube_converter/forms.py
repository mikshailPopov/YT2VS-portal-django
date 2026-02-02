from django import forms


class UrlForm(forms.Form):
    youtube_url = forms.CharField(label="url", max_length=100)
    min_range = forms.CharField(label="min_range", max_length=100)
    max_range = forms.CharField(label="max_range", max_length=100)
    formats = forms.CharField(label="formats", max_length=100)
