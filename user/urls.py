from django.urls import path
from .views import (Register, Login, Manageprofile, LogoutView, ChangePasswordView, Forgetpassword, Resetpassword)

urlpatterns = [
    path('register', Register.as_view()),
    path('login', Login.as_view()),
    path('manage', Manageprofile.as_view()),
    path('logout', LogoutView.as_view()),
    path('change_password', ChangePasswordView.as_view()),
    path('forget_password',Forgetpassword.as_view()),
    path('reset_password/<Reset_link>', Resetpassword.as_view()),
]