# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PremiumPackagesViewSet

router = DefaultRouter()
router.register(r'packages', PremiumPackagesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
