from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import CustomUser


class SignUpForm(UserCreationForm):

    name = forms.CharField(max_length=50,required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(max_length=255, required=True, help_text="To get sample,please enter your delivery address", widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2','name','address', 'avatar']

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered')
        return email

