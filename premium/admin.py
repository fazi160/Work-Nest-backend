from django.contrib import admin

# Register your models here.
from .models import PremiumPackages, PremiumCustomer

admin.site.register(PremiumPackages)
admin.site.register(PremiumCustomer)

