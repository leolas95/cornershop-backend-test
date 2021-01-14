from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import LoginEmployeeView, SignUpManagerView, SignUpEmployeeView, ProfileView

app_name = 'users'
urlpatterns = [
    path('login/', LoginEmployeeView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('manager/signup/', SignUpManagerView.as_view(), name='signup_manager'),
    path('employee/signup/', SignUpEmployeeView.as_view(), name='signup_employee'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
