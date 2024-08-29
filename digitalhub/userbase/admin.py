from django.contrib import admin
from .models import Company_Category, Company, Preference
# Register your models here.

admin.site.register(Company)
admin.site.register(Company_Category)
admin.site.register(Preference)
