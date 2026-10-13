from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobSourceViewSet

router = DefaultRouter()
router.register(r'sources', JobSourceViewSet, basename='jobsource')

urlpatterns = [
    path('', include(router.urls)),
]
