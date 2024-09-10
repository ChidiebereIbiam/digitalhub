from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import BundlePlan, StandAlonePlan, Subscription, Invoice, PaymentMethod
import stripe


def handle_checkout_session_completed(session):
    print(session)
    payment_intent_id = session.get("payment_intent")
    customer_email = session.get("customer_email")
    user = get_user_model().objects.filter(email=customer_email).first()
    stripe_customer_id = session.get('customer')
    stripe_subscription_id = session.get('subscription')

    plan_id = None
    standalone_plan_id = None

    # Create a subscription entry
    plan_type = session.get("metadata", {}).get("plan_type")
    if plan_type == "bundle":
        plan_id = session.get("metadata", {}).get("plan_id")
    elif plan_type =="standalone":
        standalone_plan_id = session.get("metadata", {}).get("plan_id")

    plan = BundlePlan.objects.filter(id=plan_id).first() if plan_id else None
    standalone_plan = (
        StandAlonePlan.objects.filter(id=standalone_plan_id).first()
        if standalone_plan_id
        else None
    )

    Subscription.objects.create(
        user=user,
        plan=plan,
        standalone_plan=standalone_plan,
        end_date=timezone.now() + timedelta(days=30),
        stripeCustomerId=stripe_customer_id,
        stripeSubscriptionId=stripe_subscription_id,
    )

    # Check and create a payment method if it doesn't exist
    if payment_intent_id:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        print(f"payment intent {payment_intent}")
        payment_method_id = payment_intent.payment_method
        print(f"payment_method_id {payment_method_id}")
        if payment_method_id:
            payment_method = stripe.PaymentMethod.retrieve(payment_method_id)

            print(f"payment method {payment_method}")
            if payment_method and payment_method.card:
                card = payment_method.card
                card_brand = card.brand
                card_last4 = card.last4  # Last 4 digits of the card

                # Convert card expiration month and year to a date
                expiration_date = timezone.datetime(
                    year=card.exp_year, month=card.exp_month, day=1
                ).date()

                # Ensure not to store full card number or CVV as per security guidelines
                PaymentMethod.objects.get_or_create(
                    user=user,
                    method=card_brand,
                    card_number=f"**** **** **** {card_last4}",
                    card_name=payment_method.billing_details.name,
                    card_expiration_date=expiration_date,
                    card_cvv=payment_intent_id,
                )


def handle_invoice_payment_succeeded(invoice):
    """
    Function to handle invoice.payment_succeeded event.
    """
    # Extract relevant data from the invoice object
    customer_email = invoice["customer_email"]
    user = get_user_model().objects.filter(email=customer_email).first()

    # Extract subscription details
    subscription_id = invoice.get("subscription")
    subscription = (
        stripe.Subscription.retrieve(subscription_id) if subscription_id else None
    )

    # Determine the plan/standalone plan from metadata
    plan_id = None
    standalone_plan_id = None

    # Create a subscription entry
    plan_type = invoice.get("metadata", {}).get("plan_type")
    if plan_type == "bundle":
        plan_id = invoice.get("metadata", {}).get("plan_id")
    else:
        standalone_plan_id = invoice.get("metadata", {}).get("plan_id")
    plan = BundlePlan.objects.filter(id=plan_id).first() if plan_id else None
    standalone_plan = (
        StandAlonePlan.objects.filter(id=standalone_plan_id).first()
        if standalone_plan_id
        else None
    )

    # Create or update the Subscription entry
    if user and (plan or standalone_plan):
        Subscription.objects.update_or_create(
            user=user,
            defaults={
                "plan": plan,
                "standalone_plan": standalone_plan,
                "end_date": timezone.now() + timedelta(days=30),
            },
        )

    # Save the invoice to your model
    if user:
        Invoice.objects.create(
            user=user,
            plan=plan,
            standalone_plan=standalone_plan,
            expire_date=timezone.now() + timedelta(days=30),
            status="paid",
            invoice_id=invoice["id"],
        )
