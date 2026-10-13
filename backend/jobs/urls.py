from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, dashboard_stats, health_check

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('dashboard-stats/', dashboard_stats, name='dashboard-stats'),
    path('', include(router.urls)),
]
