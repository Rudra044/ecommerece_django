from django.urls import path
from .views import (Register, Login, Manageprofile, LogoutView,
                    ChangePassword, Forgetpassword, Resetpassword)

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('manage/', Manageprofile.as_view(), name='manage'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/', ChangePassword.as_view(), name='change_password'),
    path('forget_password/', Forgetpassword.as_view(), name='forget_password'),
    path('reset_password/<Reset_link>/', Resetpassword.as_view(), name='reset_password'),
]
