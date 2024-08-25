from django.shortcuts import get_object_or_404, render
from digitalhub.core.models import Service
from .models import BundlePlan, StandAlonePlan, PaymentMethod, Subscription
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from .utils import handle_checkout_session_completed, handle_invoice_payment_succeeded


# Create your views here.
def pricing(request):
    services = Service.objects.all()
    plans = BundlePlan.objects.all()
    return render(
        request, "payment/pricing.html", {"services": services, "plans": plans}
    )


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == "GET":
        plan_id = 1
        standalone_plan_id = None
        domain_url = "http://127.0.0.1:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancelled/",
                payment_method_types=["card"],
                mode="subscription",
                line_items=[
                    {
                        "quantity": 1,
                        "price": "price_1PqxDbEDrn38YdUQ5pxEPmME",
                    }
                ],
                customer_email=request.user.email,
                metadata={
                    "plan_id": plan_id,
                    "standalone_plan_id": standalone_plan_id,
                },
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


class SuccessView(TemplateView):
    template_name = "payment/payment_success.html"


class CancelledView(TemplateView):
    template_name = "payment/payment_cancelled.html"


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    event = None

    # Construct the Stripe event
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the 'checkout.session.completed' event
    if event["type"] == "checkout.session.completed":
        print(event)
        session = event["data"]["object"]
        handle_checkout_session_completed(session)
    #TODO TEST THIS WEBHOOK
    elif event["type"] == "invoice.payment_succeeded":
        # Handle invoice.payment_succeeded for subscription payments
        invoice = event["data"]["object"]
        handle_invoice_payment_succeeded(invoice)
    return HttpResponse(status=200)


#TODO ENSURE TO MAKE THIS WORK WHEN WORKING WITH TEMPLATE
@csrf_exempt
def cancel_subscription(request, subscription_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == "POST":
        try:
            # Retrieve the subscription from Stripe
            subscription = stripe.Subscription.retrieve(subscription_id)
            
            # Cancel the subscription
            canceled_subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True 
            )

            # Update your database record if needed
            db_subscription = get_object_or_404(Subscription, id=subscription_id)
            db_subscription.status = 'canceled'
            db_subscription.save()

            return JsonResponse({"status": "Subscription canceled", "subscription": canceled_subscription})
        except stripe.error.StripeError as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)