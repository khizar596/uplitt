from django.urls import path
from .views import RegisterView,LoginApiView,VerifyEmail,OtpView,Otpsend,Sendverifyemail

urlpatterns=[
    path('register/',RegisterView.as_view(),name='Registration'),
    path('login/',LoginApiView.as_view(),name='Login'),
    path('email_verify/',VerifyEmail.as_view(),name='email_verify'),
    # path('reset_password/',passwordresetemail.as_view(),name='password_reset'),
    path('sendotp/',Otpsend.as_view(),name='Send OTP'),
    path('sendemail/',Sendverifyemail.as_view(),name='Send email'),
    path('otpverify/',OtpView.as_view(),name='OTPCONFIRMATION')
]


