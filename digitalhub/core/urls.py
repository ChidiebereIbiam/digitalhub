from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about-us/', views.about, name="about_us"),
    path('contact-us/', views.contact_us, name="contact_us"),
    path('faq/', views.faq, name="faq"),
    path('privacy-policy/', views.privacy_policy, name="privacy_policy"),
    path('pricing/', views.pricing, name="pricing"),
    path("services", views.services, name="services"),
    path('service/<slug:slug>', views.service_details, name="service_details"),
]
