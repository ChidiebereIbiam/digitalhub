from django.contrib import admin
from .models import Service, Plan, Benefit, Review, Team

admin.site.register(Service)
admin.site.register(Plan)
admin.site.register(Benefit)
admin.site.register(Review)
admin.site.register(Team)

