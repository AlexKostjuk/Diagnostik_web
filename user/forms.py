from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=200, required=True)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=True)
