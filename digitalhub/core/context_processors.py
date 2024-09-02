from .models import Service

def persistent_settings(request):
    context = {
        "phone1": "+447 909736637494",
        "phone2":"+635548384793999",
        "address": "Test location Enugu",
        "email": "support@digitalhub247.com"
    }
    try:
        services = Service.objects.all()
        
    except Service.DoesNotExist:
        services = None
    if services:
        context["services"]=services
    return context