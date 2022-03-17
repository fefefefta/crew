from django.forms import ModelForm

from .models import User


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'bio']
