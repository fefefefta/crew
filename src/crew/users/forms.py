from django import forms

from .models import User


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'bio']
    username = forms.CharField(
            label='',
            max_length=30,
            strip=True,
            widget=forms.TextInput(attrs={
                    "class": "registration-field username-field",
                    "placeholder": "username",
                }
            )
        )
    full_name = forms.CharField(
            label='',
            max_length=40,
            strip=True,
            widget=forms.TextInput(attrs={
                    "class": "registration-field fullname-field",
                    "placeholder": "имя или псевдоним",
                }
            )
        )
    email = forms.EmailField(
            label='',
            widget=forms.EmailInput(attrs={
                    "class": "registration-field email-field",
                    "placeholder": "email",
                }
            )
        )
    bio = forms.CharField(
            label='',
            widget=forms.Textarea(attrs={
                    "class": "registration-bio",
                    "placeholder": "напиши о себе",
                }
            )
        )


class UserProfileEdit(UserRegistrationForm):
    username = forms.CharField(
            disabled=True,
            widget=forms.TextInput(attrs={
                    "class": "registration-field username-field",
                    "placeholder": "username",
                }
            )
        )

