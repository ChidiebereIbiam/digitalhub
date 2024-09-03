from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
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
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .utils import handle_checkout_session_completed, handle_invoice_payment_succeeded


# Create your views here.
def pricing(request):
    services = Service.objects.all()
    

    
    try:
        basic_plan = BundlePlan.objects.get(title__iexact="basic plan")
        social_media_service = Service.objects.get(title__iexact="Social Media Management")
        standalone_plans = social_media_service.stand_alone_plans.all()
    except:
        standalone_plans = None
        basic_plan= None


    return render(
        request, "payment/pricing.html", 
        {
            "services": services, 
            "basic_plan": basic_plan,
            "standalone_plans":standalone_plans}
    )


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@login_required
def create_checkout_session(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect(reverse("account_login"))

    if request.method == "GET":
        # Retrieve plan_id and plan_type from GET request parameters
        plan_id = request.GET.get('id')
        plan_type = request.GET.get('plan_type')

        if plan_type == "bundle":
            plan = BundlePlan.objects.get(id=plan_id)
        elif plan_type=="standalone":
            plan = StandAlonePlan.objects.get(id=plan_id)

        if not plan_id or not plan_type:
            return JsonResponse({"error": "Missing plan_id or plan_type"}, status=400)

        domain_url = settings.DOMAIN_URL.rstrip('/') + '/'
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            # Create the checkout session
            checkout_session = stripe.checkout.Session.create(
                success_url=request.build_absolute_uri(reverse("payment_success")),
                cancel_url=request.build_absolute_uri(reverse("payment_cancel")),
                payment_method_types=["card"],
                mode=plan.payment_mode,
                line_items=[
                    {
                        "quantity": 1,
                        "price": plan.price_id,
                    }
                ],
                customer_email=request.user.email,
                metadata={
                    "plan_id": plan.id,
                    "plan_type": plan_type,
                },
            )
            # Redirect the user to the Stripe checkout page
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

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
def cancel_subscription(request, id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # Retrieve the subscription from Stripe
    # subscription = stripe.Subscription.retrieve(id)
    
    # # Cancel the subscription
    # canceled_subscription = stripe.Subscription.modify(
    #     id,
    #     cancel_at_period_end=True 
    # )

    # Update your database record if needed
    db_subscription = get_object_or_404(Subscription, id=id)
    db_subscription.is_active = False
    db_subscription.save()

    return redirect("subscription")
