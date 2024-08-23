from django.shortcuts import render
from digitalhub.core.models import Service
from .models import BundlePlan, StandAlonePlan
from django.conf import settings
from django.http.response import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.views.generic.base import TemplateView


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
        stripe_config = {
            "publicKey": "pk_test_51Gxfo1EDrn38YdUQLMGudu7pvEBYHctDuKPmg4KRDis39dPb3coFTUjxZRrvpY1f6Q6Op0E8K2YLxobl6fc0Zuxf00AnQIBzyN"
        }
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == "GET":
        domain_url = "http://127.0.0.1:8000/"
        stripe.api_key = "sk_test_51Gxfo1EDrn38YdUQUWmgOS5851BpPPMjo6K3rDnGEoYSIep0OaeWUjQev4F3RVTeNC4AbYHTdiaY2DJsP0pwwg9200EwitDbjp"
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancelled/",
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "quantity": 1,
                        "price": "price_1PqtmXEDrn38YdUQXGwN1K8e",
                    }
                ],
                customer_email=request.user.email
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
    stripe.api_key = "sk_test_51Gxfo1EDrn38YdUQUWmgOS5851BpPPMjo6K3rDnGEoYSIep0OaeWUjQev4F3RVTeNC4AbYHTdiaY2DJsP0pwwg9200EwitDbjp"
    endpoint_secret = "whsec_776a16c71f443b2600a77c95b1f6171e4c460d6f8dade1081728c2f18e3e19c6"
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        print(event)
        # TODO: run some custom code here

    return HttpResponse(status=200)