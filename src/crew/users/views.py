from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView

from .forms import UserRegistrationForm, UserProfileEdit
from .models import LoginCode, User
from .services import initiate_email_confirmation, finish_email_confirmation, \
    send_login_code_to_user
from crew.settings import STATUS_ON_MODERATION
from utils.notifications import notify_staff_approve_user, \
    notify_user_profile_approve_decision
from utils.decorators import staff_only


class UserRegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'

    # Page with message about sended confirmation letter
    success_url = '/reg/confirm-email/'

    def form_valid(self, form):
        user = form.save()

        notify_staff_approve_user(user)
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
                'error':  'some error occured',
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
            return redirect('events')

        return HttpResponse('нЕ РоБоТаИт(((((:((((')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class UserDetailView(DetailView):
    model = User
    object_context_name = 'user'
    template_name = 'users/profile.html'

    def get(self, request, username, *args, **kwargs):
        if username == 'me':
            return redirect('profile', request.user.username)
        return super().get(request, username, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request_user'] = self.request.user
        return context

    def get_object(self):
        username = self.kwargs.get('username')
        user = User.get_user_by_username(username)
        if (user.is_approved() or self.request.user.is_staff
                or self.request.user == user):
            return user

        raise Exception('u r not allowed to be here zhulic')


class UserProfileEditView(UpdateView):
    # model = User
    form_class = UserProfileEdit
    object_context_name = 'user'
    # fields = ['full_name', 'email', 'bio']
    template_name = 'users/profile_edit.html'
    success_url = '/user/me'

    def get_object(self):
        user = User.get_user_by_username(self.kwargs.get('username'))
        if user == self.request.user and not user.is_on_moderation():
            return user

        raise Exception('u r not allowed to be here zhulic')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.moderation_status = STATUS_ON_MODERATION
        self.object.save()

        notify_staff_approve_user(self.object)

        if 'email' in form.changed_data:
            self.object.deactivate()
            initiate_email_confirmation(self.object)
            logout(self.request)
            return redirect('login')

        return super().form_valid(form)


@staff_only
def user_approve(request, username):
    user = User.get_user_by_username(username)
    if not user.is_approved():
        user.approve()

        notify_user_profile_approve_decision(user)

        return redirect('profile', username)

    raise Exception('u r not allowed to be here zhulic')


@staff_only
def user_decline(request, username):
    user = User.get_user_by_username(username)

    if request.method == 'GET':
        return render(request, 'users/user_decline.html', {'user': user})

    if not user.is_declined():
        user.decline()

        comment = request.POST.get('comment')
        notify_user_profile_approve_decision(user, comment=comment)

    return redirect('profile', username)
