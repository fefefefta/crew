from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView

from .forms import UserRegistrationForm
from .models import EmailConfirmationCode
from .services import initiate_email_confirmation, finish_email_confirmation


class UserRegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    
    # Page with message about sended confirmation letter
    success_url = '/reg/confirm-email/'

    def form_valid(self, form):
        user = form.save()

        # Creating user-code object and sending letter to user email
        initiate_email_confirmation(user)
        return super().form_valid(form)


class EmailConfirmationView(View):
    """
    Processes the click on the link containing the secret code to 
    confirm the email.

    """

    def get(self, request, **kwargs):
        confirmation_code = self.kwargs['confirmation_code']
        
        # Turning user.is_active on True and deleting user-code object
        finish_email_confirmation(confirmation_code)
        return HttpResponse("Почта подтверждена.")

