# from twilio.rest import Client
# Create your models here.
from django.db import models
class User(models.Model):
    email = models.CharField(max_length=80, unique=True, help_text='Email')
    password = models.CharField(max_length=80, blank=False,help_text='Phone_number')
    OTP=models.IntegerField(null=True,blank=True)
    phone_number = models.CharField(max_length=20, unique=True, help_text='Phone_number')
    created=models.DateTimeField(auto_now=True)
    token=models.CharField(blank=True,max_length=100)
    user_active=models.BooleanField(default=False)
    OTP_verified_user=models.BooleanField(default=False)
    email_verified_user=models.BooleanField(default=False)
    # reset_token=models.CharField(blank=True,max_length=100)
    def __str__(self):
        return self.email




















    # def save(self,*args,**kwargs):
    #     account_sid = 'AC6c9d7dcd896050c754bf77761981dca4'
    #     auth_token = '7a0949a9035685aa1937830d57a39342'
    #     client = Client(account_sid, auth_token)
    #
    #     message = client.messages.create(
    #         body=f'Your verification code is : {self.OTP}  ',
    #         from_='+12513086017',
    #         to=f'{self.phone_number}'
    #     )
    #
    #     return super().save(*args,**kwargs)
