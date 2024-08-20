from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# Create your views here.

def home(request):
    return render(request, 'core/homepage.html')


def about(request):
    return render(request, 'core/about.html')


def contact_us(request):
    if request.method == "POST":
        name = request.POST['name']
        email_from = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        context = {
            "name": name,
            "email": email_from,
            "subject": subject,
            "message": message
        }

        html_content = render_to_string('email/contact_us_email.html', context)
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
            
            messages.success(request, 'Thanks for Contacting Us, we will get back to you shortly')
        except:
            messages.error(request, 'An error occured, try again')

        redirect("contact_us")
    return render(request, 'core/contact_us.html')


def faq(request):
    return render(request, 'core/faq.html')

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')


def pricing(request):
    return render(request, 'core/pricing.html')
