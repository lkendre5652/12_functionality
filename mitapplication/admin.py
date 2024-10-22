from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, OTPVerify


class OTPVerifyAdmin(admin.ModelAdmin):
    list_display = ['id', 'otp_my', 'email', 'client_ip', 'verify_otp', 'created_at', 'updated_at']
    list_display_links = ['id', 'otp_my', 'email', 'client_ip', 'verify_otp', 'created_at', 'updated_at']

admin.site.register(OTPVerify,OTPVerifyAdmin)

class AccountAdmin(UserAdmin):
    list_display = ('id','email','first_name','last_name','username','last_login','date_joined','is_active')
    list_display_links = ( 'email','first_name','last_name' )
    readonly_fields = ( 'last_login','date_joined' )
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Account, AccountAdmin)
