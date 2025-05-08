from django.urls import path

from .views import GetOTPView, RegistrationView

urlpatterns = [
    path("generate_otp/", GetOTPView().as_view(), name="generate-otp"),
    path("register/", RegistrationView().as_view(), name="register"),
]
