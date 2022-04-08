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
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from users.models import LoginCode

from users.views import LoginView, UserRegistrationView, \
    EmailConfirmationView, LoginView, LoginCodeView, UserProfileView, \
    UserProfileEditView, LogoutView
from events.views import FeedView, EventDetailView, EventCreateView, \
    EventEditView, event_approve


urlpatterns = [
    path('admin/', admin.site.urls),
    # registration
    path('reg/', UserRegistrationView.as_view(), name='registration'),
    path('reg/confirmation/<confirmation_code>/', 
         EmailConfirmationView.as_view(),
         name='email_confirmation'),
    # login
    path('login/', LoginView.as_view(), name='login'),
    path('login/code/', LoginCodeView.as_view(), name='login_code'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # users
    path('user/<username>/',
         login_required(UserProfileView.as_view()),
         name='profile'),
    path('user/<username>/edit/',
         login_required(UserProfileEditView.as_view()),
         name='profile_edit'),
    # events
    path('', FeedView.as_view(), name=''),
    path('events/', FeedView.as_view(), name='events'),
    path('events/<int:pk>/', 
         login_required(EventDetailView.as_view()), 
         name='event'),
    path('events/new/', 
         login_required(EventCreateView.as_view()), 
         name='event_new'),
    path('events/<int:pk>/edit/',
         login_required(EventEditView.as_view()),
         name='event_edit'),
    path('events/<int:pk>/approve',
         event_approve,
         name='event_approve'),
]
