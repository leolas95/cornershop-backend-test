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
from django.urls import path
from django.views.generic import TemplateView

from users.views import SignUpManagerView, SignUpEmployeeView, LoginEmployeeView, ProfileView

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('users/login/', LoginEmployeeView.as_view(), name='login'),
    path('users/logout/', LogoutView.as_view(), name='logout'),
    path('users/manager/signup/', SignUpManagerView.as_view(), name='signup_manager'),
    path('users/employee/signup/', SignUpEmployeeView.as_view(), name='signup_employee'),
    path('users/profile/', ProfileView.as_view(), name='profile'),
]
