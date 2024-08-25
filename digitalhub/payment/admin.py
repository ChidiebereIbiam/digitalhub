from django.contrib import admin
from .models import BundlePlan,StandAlonePlan, PaymentMethod, Subscription

admin.site.register(BundlePlan)
admin.site.register(StandAlonePlan)
admin.site.register(PaymentMethod)
admin.site.register(Subscription)

