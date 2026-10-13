from django.urls import path  
from .views import chat

urlpatterns = [
    path('agents/chat/', chat)
]