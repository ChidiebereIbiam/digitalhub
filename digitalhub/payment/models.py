from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

PAYMENT_MODES = [
        ("payment", "Payment"),
        ("subscription", "Subscription")
]

class BundlePlan(models.Model):
    
    title = models.CharField(max_length=250)
    features = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_id = models.CharField(max_length=250)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODES, default="subscription") 

    def __str__(self):
        return f"{self.title} | {self.price}"


class StandAlonePlan(models.Model):
    DURATION_TYPES = [
        ("month", "month"),
        ("per video", "per video"),
        ("per page", "per page"),
        ("per strategy", "per strategy"),
        ("per hour", "per hour"),
        ("per setup", "per setup"),
        ("starting price", "starting price"),
    ]
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_id = models.CharField(max_length=250)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODES, default="subscription") 
    duration_type = models.CharField(max_length=50, choices=DURATION_TYPES, default="month")

    def __str__(self):
        return self.title
    

class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(BundlePlan, on_delete=models.CASCADE, null=True, blank=True)
    standalone_plan = models.ForeignKey(StandAlonePlan, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    stripeCustomerId = models.CharField(max_length=255, null=True, blank=True)
    stripeSubscriptionId = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return f"{self.user.email} | {self.plan.title if self.plan else self.standalone_plan}"


class PaymentMethod(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.CharField(max_length=50)
    card_number = models.CharField(max_length=50)
    card_name = models.CharField(max_length=250)
    card_expiration_date = models.DateField()
    card_cvv = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.email} | {self.method}"

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(BundlePlan, on_delete=models.CASCADE, null=True, blank=True)
    standalone_plan = models.ForeignKey(StandAlonePlan, on_delete=models.CASCADE, null=True, blank=True)
    issue_date = models.DateField(auto_now_add=True)
    expire_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50)
    invoice_id = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.user.email} | {self.plan.title if self.plan else self.standalone_plan}"
