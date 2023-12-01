# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PremiumPackagesViewSet, StripePayment, PremiumPackagesViewOnly, PaymentSuccess, PremiumSalesReport

router = DefaultRouter()
router.register(r'packages', PremiumPackagesViewSet, basename="packages")
router.register(r'packagesview', PremiumPackagesViewOnly, basename="packages_view")




urlpatterns = [
    path('', include(router.urls)),
    path('payment/', StripePayment.as_view(), name = 'premium_payment'),
    path('paymentsuccess/', PaymentSuccess.as_view(), name = 'PaymentSuccess'),
    path('premiumsales/', PremiumSalesReport.as_view(), name='PremiumSales'),
]
