from django.contrib import admin
from .models import User
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email','phone_number','token','created','OTP','OTP_verified_user','email_verified_user']
