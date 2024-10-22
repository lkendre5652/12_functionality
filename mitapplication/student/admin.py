from django.contrib import admin
from .models import OTPVerify, Form2019Payment1

class Form2019Payment1Admin(admin.ModelAdmin):
    list_display = ['order_id']
    list_display_links = ['order_id']
admin.site.register(Form2019Payment1,Form2019Payment1Admin)

class OTPVerifyAdmin(admin.ModelAdmin):
    list_display = ['id', 'otp_my', 'email', 'client_ip', 'verify_otp', 'created_at', 'updated_at']
    list_display_links = ['id', 'otp_my', 'email', 'client_ip', 'verify_otp', 'created_at', 'updated_at']

admin.site.register(OTPVerify,OTPVerifyAdmin)
