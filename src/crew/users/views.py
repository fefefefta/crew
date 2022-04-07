from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import FormView, UpdateView

from .forms import UserRegistrationForm
from .models import LoginCode, User
from .services import initiate_email_confirmation, finish_email_confirmation, \
    send_login_code_to_user


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
        user = User.get_user_by_email(email)

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

        user = User.get_user_by_username(username)
        return render(request, 'users/profile.html', {
                'user': user,
                'requesting_user': request.user,
            })


class UserProfileEditView(UpdateView):
    model = User
    fields = ['full_name', 'bio']
    template_name = 'users/profile_edit.html'
    success_url = '/user/me'

    def get_object(self):
        user = User.get_user_by_username(self.kwargs.get('username'))
        if user.username == self.request.user.username:
            return user

        raise Exception('u r not allowed to be here zhulic')
