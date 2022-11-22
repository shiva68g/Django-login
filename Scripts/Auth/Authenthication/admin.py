from django.contrib import admin
from .models import *

@admin.register(MyUser)
class Myuser(admin.ModelAdmin):
	list_display = ['id' , 'name' , 'date_of_birth' , 'is_verified' , 'is_admin']

@admin.register(OtpCode)
class Otp(admin.ModelAdmin):
	list_display = [ 'id' ,'User','code']