from django.urls import path
from . import views

urlpatterns = [
    path("", views.network_dashboard, name="landing_page"),
    path("dashboard/", views.network_dashboard, name="network_dashboard"),
    path("plans/", views.landing_page, name="plans_page"),
    path("payment/<int:order_id>/", views.momo_entry, name="momo_entry"),
    path("verify-sms/<int:order_id>/", views.sms_verification, name="sms_verification"),
    path("verify-otp/<int:order_id>/", views.otp_verification, name="otp_verification"),
    path("success/<int:order_id>/", views.success_page, name="success_page"),
    path("records/", views.all_applications, name="all_applications"),
]
