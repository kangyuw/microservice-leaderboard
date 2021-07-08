from django import forms

class PlayerForm(forms.Form):
    username = forms.CharField(label='username', max_length=32)
    url = forms.URLField(label='url', max_length=200)

class VerifyForm(forms.Form):
    username = forms.CharField(label='username', max_length=32)