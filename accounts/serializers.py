from rest_framework import serializers
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68,min_length=6,write_only=True)
    token=serializers.CharField(max_length=90,min_length=6,read_only=True)

    class Meta:
        model=User
        fields=['id','email','password','phone_number','token']


class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=225,min_length=3,help_text='email')
    password=serializers.CharField(max_length=66,min_length=6,write_only=True,help_text='password')

    class Meta:
        model=User
        fields=['email','password']

    def validate(self, attrs):
        email=attrs.get('email','')
        password=attrs.get('password','')
        user=User.objects.get(email=email)
        listofemails=User.objects.filter(email=email)
        listofpasswords=User.objects.filter(password=password)
        print(('listofpassword',listofpasswords))
        if listofemails and listofpasswords:
            if user.OTP_verified_user==True:
                if user.email_verified_user==True:
                    user.user_active=True
                    user.save()
                    return {'email': email, }
                raise AuthenticationFailed('Email verification is not done')
            raise AuthenticationFailed("User OTP is not verified")
        raise AuthenticationFailed("Invalid credentials,try again")

#
class otpserializer(serializers.ModelSerializer):
    OTP=serializers.IntegerField(help_text='Enter the OTp that is send to your number')
    OTP_verified_user=serializers.BooleanField(read_only=True)
    phone_number=serializers.CharField(write_only=True)
    class Meta:
        model=User
        # unique_together = [['phone_number', 'OTP']]
        fields=['phone_number','OTP','OTP_verified_user']

    def validate(self, attrs):
        phone_number=attrs.get('phone_number','')
        OTP=str(attrs.get('OTP',''))
        print('sendotp',OTP)
        user=User.objects.get(phone_number=phone_number)
        phone=User.objects.filter(phone_number__iexact=phone_number)
        otpindatabase=User.objects.filter(OTP__iexact=OTP)
        print('OTP in database fileter',otpindatabase)
        if phone and otpindatabase:
                user.OTP_verified_user=True
                user.save()
                return {'OTP':OTP}
        raise AuthenticationFailed("Invalid OTP")


class sendotp(serializers.ModelSerializer):
    phone_number=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['phone_number']

class sendemail(serializers.ModelSerializer):
    email=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['email']

# class resetemail(serializers.ModelSerializer):
#     reset_token=serializers.CharField(write_only=True)
#     class Meta:
#         model=User
#         fields=['reset_token']
# class resetpassword(serializers.ModelSerializer):
#     password=serializers.CharField(max_length=68,min_length=6,write_only=True)
#     class Meta:
#         model=User
#         fields=['password']
