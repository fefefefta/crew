from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import FormView

from .forms import UserRegistrationForm
from .models import LoginCode
from .services import initiate_email_confirmation, finish_email_confirmation, \
    get_user_by_email, send_login_code_to_user


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
        if request.user.is_authenticated:
            return redirect('profile', request.user.username)

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
    def get(self, request):
        return redirect('login')

    def post(self, request):
        email = request.POST.get('email')
        code = request.POST.get('code')

        user = authenticate(email=email, code=code)
        if user:
            login(request, user)
            return HttpResponse('все получилось!!!')

        return HttpResponse('нЕ РоБоТаИт(((((:((((')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class UserProfileView(View):
    def get(self, request, username: str):
        if username == 'me':
            return redirect('profile', request.user.username)

        if request.user.is_staff:
            return HttpResponse(f"{username}'s profile. and u r moderator!")

        if request.user.username == username:
            return HttpResponse('u r at home')
        
        return HttpResponse(f"{username}'s profile")
        
