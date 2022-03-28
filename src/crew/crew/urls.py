"""crew URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.models import LoginCode

from users.views import LoginView, UserRegistrationView, \
    EmailConfirmationView, LoginView, LoginCodeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/', UserRegistrationView.as_view(), name='registration'),
    path('reg/confirmation/<confirmation_code>', 
         EmailConfirmationView.as_view(),
         name='email_confirmation'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/code/', LoginCodeView.as_view(), name='login_code'),
]
