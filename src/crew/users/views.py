from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView

from .forms import UserRegistrationForm
from .models import LoginCode
from .services import initiate_email_confirmation, finish_email_confirmation, \
    get_user_by_email, send_login_code_to_user
from utils.email import send_crew_email


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


class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        email = request.POST.get('email')
        user = get_user_by_email(email)       

        if user.is_active:
            code = LoginCode.create_for_user(user).code            
            send_login_code_to_user(user, code)

            return render(request, "users/login_code.html", {
                    'email': email
                })

        initiate_email_confirmation(user)

        return render(request, "users/login.html", {
                'email_not_confirmed':  True,
            })


class LoginCodeView(View):
    def post(self, request):
        email = request.POST.get('email')
        code = request.POST.get('code')
        print(request.user.is_authenticated)

        username = get_user_by_email(email).username
        user = authenticate(username=username, code=code)
        if not user:
            return HttpResponse('нЕ РоБоТаИт(((((:((((')

        return HttpResponse('все получилось!!!')



        

        

