from .models import Service

def persistent_settings(request):
    context = {}
    try:
        services = Service.objects.all()
        
    except Service.DoesNotExist:
        services = None
    if services:
        context["services"]=services
    return context