from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SavedJobViewSet, JobApplicationViewSet

router = DefaultRouter()
router.register(r'saved-jobs', SavedJobViewSet, basename='savedjob')
router.register(r'tracker', JobApplicationViewSet, basename='jobapplication')

urlpatterns = [
    path('', include(router.urls)),
]
