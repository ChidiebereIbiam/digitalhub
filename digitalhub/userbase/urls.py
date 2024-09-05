from django.urls import path
from .views import (
    edit_profile,
    user_change_profile_picture,
    subscription,
    invoice,
    payment_method,
    delete_payment_method,
    preference,
    toggle_preference,
    PasswordsChangeView,
    Password_Success
)

urlpatterns = [
    path("edit/", edit_profile, name="edit_profile"),
    path(
        "change-profile-picture/",
        user_change_profile_picture,
        name="user_change_profile_picture",
    ),
    path("subscriptions/", subscription, name="subscription"),
    path("invoices/", invoice, name="invoice"),
    path("payment-methods/", payment_method, name="payment_method"),
    path(
        "delete-payment-method/<str:id>",
        delete_payment_method,
        name="delete_payment_method",
    ),
    path("preferences/", preference, name="preference"),
    path(
        "preference/toggle/<str:preference>/",
        toggle_preference,
        name="toggle_preference",
    ),
    path('password/', PasswordsChangeView.as_view(template_name='userbase/change-password.html'), name="change_password"),
    path('password_success/', Password_Success, name='password_success'),
]
