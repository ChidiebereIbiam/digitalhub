from .models import Service

def persistent_settings(request):
    context = {
        "phone1": "210.845.9990",
        "phone2":"",
        "address": "18756 Stone Oak Parkway, suite 200 San Antonio Texas 78358",
        "email": "contact@247digitalhub.com"
    }
    try:
        services = Service.objects.all()
        
    except Service.DoesNotExist:
        services = None
    if services:
        context["services"]=services
    return context