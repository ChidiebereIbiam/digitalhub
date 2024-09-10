from django.urls import path
from .import views

urlpatterns = [
    path('pricing/', views.pricing, name="pricing"),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.SuccessView.as_view(), name="payment_success"),
    path('cancelled/', views.CancelledView.as_view(), name="payment_cancel"),
    path('webhook/', views.stripe_webhook),
    path('cancel-subscription/<str:stripeSubscriptionId>', views.cancel_subscription, name="cancel_subscription")
]
