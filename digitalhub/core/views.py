from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Review, Service, Team
from digitalhub.blog.models import Post
from digitalhub.payment.models import BundlePlan, StandAlonePlan

# Create your views here.


def home(request):
    posts = Post.objects.all()[0:3]
    plans = BundlePlan.objects.all()
    services = Service.objects.all()
    reviews = Review.objects.all()

    context = {"posts": posts, "plans": plans, "services": services, "reviews": reviews}
    return render(request, "core/homepage.html", context)


def about(request):
    services = Service.objects.all()
    teams = Team.objects.all()
    context = {"services": services, "teams": teams}
    return render(request, "core/about.html", context)


def contact_us(request):
    services = Service.objects.all()

    if request.method == "POST":
        name = request.POST["name"]
        email_from = request.POST["email"]
        subject = request.POST["subject"]
        message = request.POST["message"]

        context = {
            "name": name,
            "email": email_from,
            "subject": subject,
            "message": message,
        }

        html_content = render_to_string("email/contact_us_email.html", context)
        text_content = strip_tags(html_content)

        try:
            email = EmailMultiAlternatives(
                subject=f"New Contact Us Message from {name}",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.DEFAULT_EMAIL],
            )

            email.attach_alternative(html_content, "text/html")

            # Send the email
            email.send()

            messages.success(
                request, "Thanks for Contacting Us, we will get back to you shortly"
            )
        except:
            messages.error(request, "An error occured, try again")

        redirect("contact_us")
    return render(request, "core/contact_us.html", {"services": services})


def faq(request):
    services = Service.objects.all()
    return render(request, "core/faq.html", {"services": services})


def privacy_policy(request):
    services = Service.objects.all()
    return render(request, "core/privacy_policy.html", {"services": services})


def pricing(request):
    services = Service.objects.all()
    return render(request, "core/pricing.html", {"services": services})


def services(request):
    services = Service.objects.all()
    context = {"services": services}
    return render(request, "core/services.html", context)


def service_details(request, slug):
    services = Service.objects.all()
    service = get_object_or_404(Service, slug=slug)
    context = {"services": services, "service": service}
    return render(request, "core/service-details.html", context)
