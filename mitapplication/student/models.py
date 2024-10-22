from django.db import models
from django.utils import timezone

class OTPVerify(models.Model):
    otp_my = models.CharField(max_length=7, blank=False, verbose_name="OTP")
    email = models.EmailField(max_length=100, blank=False, verbose_name="E-mail")
    client_ip = models.CharField(max_length=12, blank=True, verbose_name="Client IP Address")
    verify_otp = models.BooleanField(default=False, verbose_name="Verify OTP")    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.otp_my

    class Meta:
        verbose_name = "OTPVerify"
        verbose_name_plural = "OTP Verify"


from django.db import models

from django.db import models

class Form2019Payment1(models.Model):
    order_id = models.CharField(max_length=255)
    course = models.CharField(max_length=255, default='')
    first_name = models.CharField(max_length=255, default='')
    middle_name = models.CharField(max_length=255, default='', blank=True, null=True)
    last_name = models.CharField(max_length=255, default='')    
    email = models.EmailField(default='')
    phone = models.CharField(max_length=20, default='')
    address = models.TextField(default='')
    city = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    pincode = models.CharField(max_length=20, default='')
    category = models.CharField(max_length=255, default='')
    gender = models.CharField(max_length=10, default='')
    nationality = models.CharField(max_length=255, default='')
    currency = models.CharField(max_length=3, default='INR')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.order_id



