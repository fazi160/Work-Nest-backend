# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PremiumPackagesViewSet, StripePayment, PremiumPackagesViewOnly

router = DefaultRouter()
router.register(r'packages', PremiumPackagesViewSet)
router.register(r'packagesview', PremiumPackagesViewOnly)


urlpatterns = [
    path('', include(router.urls)),
    path('payment/', StripePayment.as_view(), name = 'premium_payment')
]
