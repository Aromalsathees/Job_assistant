from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiscoveryRunViewSet

router = DefaultRouter()
router.register(r'runs', DiscoveryRunViewSet, basename='discoveryrun')

urlpatterns = [
    path('', include(router.urls)),
]
