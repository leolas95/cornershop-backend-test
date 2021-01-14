"""cornershop_backend_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
# from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from menus.views import CreateMenuView, DetailMenuView, ListMenuView
from slack.views import SendReminderView, SelectMenuOptionView
from users.views import SignUpManagerView, SignUpEmployeeView, LoginEmployeeView, ProfileView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('users/', include('users.urls')),
    path('menu/create/', CreateMenuView.as_view(), name='create_menu'),
    path('menu/detail/<int:pk>/', DetailMenuView.as_view(), name='detail_menu'),
    path('menu/', ListMenuView.as_view(), name='list_menus'),
    path('menu/send_reminder/<int:menu_id>', SendReminderView.as_view(), name='send_reminder'),
    path('menu/<uuid:selection_uuid>/', SelectMenuOptionView.as_view(), name='select_menu_option'),
]
