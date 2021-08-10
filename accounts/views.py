from twilio.rest import Client
import time
from django.shortcuts import render
from .stringgenerator import string_generator,OTP_numbr
from rest_framework import generics,status
from .serializers import UserSerializer,LoginSerializer,otpserializer,sendotp,sendemail
from django.core.mail import EmailMessage
from rest_framework.response import Response
from .utils import Util
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    def post(self,request):

       user=request.data
       serializer=self.serializer_class(data=user)
       serializer.is_valid(raise_exception=True)
       token=string_generator()#generating a token
       serializer.validated_data['token']=token
       serializer.save()
       return Response({'Message':'Succesfully registered ',
                         'token':f'{token}'},
                        status=status.HTTP_201_CREATED)

class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data['OTP_verified_user']=True
        return Response(
            {'Title':'Login Succesfylly','message':'Congratulations to be a part of Uplit'},status=status.HTTP_200_OK
            )


#
class OtpView(generics.GenericAPIView):
    serializer_class = otpserializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Succesfuly verified'})


class VerifyEmail(generics.GenericAPIView):
    def get(self,request):
        token=request.GET.get('token')
        user=User.objects.get(token=token)
        if user:
            user.email_verified_user=True
            user.save()
            return Response({
                'Message':'Email verified succesfully.'
            })
        return Response('Invalid key')


class Sendverifyemail(generics.GenericAPIView):
    serializer_class = sendemail
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        email = serializer.validated_data['email']
        user=User.objects.get(email=email)
        token=user.token
        current_site = get_current_site(request=request).domain
        relative_link = reverse('email_verify')
        current_email = serializer.validated_data['email']
        absurl = 'http://' + current_site + relative_link + "?token=" + str(token)
        email_body = 'Hi ' + current_email + 'Use Link below to verify your email \n' + absurl
        data = {
            'email_body': email_body,
            'to_email': current_email,
            'email_subject': 'Verify Your email'
        }
        Util.send_email(data=data)
        return Response('Verification link has been sent')

class Otpsend(generics.GenericAPIView):
    serializer_class = sendotp
    def post(self,request):
        OTP = OTP_numbr()
        # generating OTP
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        phone_number = serializer.validated_data['phone_number']
        user = User.objects.get(phone_number=phone_number)
        phone_number = phone_number
        if user:
            user.OTP = OTP
            user.save()# saving in user's OTP coloumn
            account_sid = 'AC6c9d7dcd896050c754bf77761981dca4'
            auth_token = '543f9bfa6c79583a0570d61018a61874'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=f'Your verification code is : {OTP}  ',
                from_='+12513086017',
                to=f'{phone_number}'
            )
            return Response('OTP is sent')
        return Response('Number is not registered')


    # +++++++++++SENDING FOR PASSWORD RESET EMAIL+++++++++++

# class passwordresetemail(generics.GenericAPIView):
#     serializer_class = resetemail
#     def post(self,request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid()
#         email = serializer.validated_data['email']
#         user=User.objects.get(email=email)
#         token=user.reset_token
#         current_site = get_current_site(request=request).domain
#         relative_link = reverse('email_verify')
#         current_email = serializer.validated_data['email']
#         absurl = 'http://' + current_site + relative_link + "?token=" + str(token)
#         email_body = 'Hi ' + current_email + 'Use Link below to reset your password \n' + absurl
#         data = {
#             'email_body': email_body,
#             'to_email': current_email,
#             'email_subject': 'Password reset'
#         }
#         Util.send_email(data=data)
#         return Response('Check Your email to reset password')
#
#
# # ++++++++++++++++++++recieing email for password reset+++++++++++
#
#
# class newpassword(generics.GenericAPIView):
#     serializer_class = resetpassword
#     # def get(self,request):
#     #     token=request.GET.get('token')
#     #     user=User.objects.get(email=token)
#     #     if user:
#     #         user.email_verified_user=True
#     #         user.save()
#     #         return Response({
#     #             'Message':'Email verified succesfully.'
#     #         })
#     #     return Response('Invalid key')
#     def post(self, request):
#         token = request.GET.get('token')
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid()
#         serializer.validated_data['password']
