from django.contrib import admin
from .models import User, UserDetail, CustomerDetail
# Register your models here.
admin.site.register(User)
admin.site.register(UserDetail)
admin.site.register(CustomerDetail)