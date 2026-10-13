from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserPreference
from .serializers import UserPreferenceSerializer

class UserPreferenceView(APIView):
    """
    Get or update user job intelligence preferences.
    """
    def get(self, request):
        session_id = request.headers.get('X-Client-Session', 'default-user')
        pref, _ = UserPreference.objects.get_or_create(client_session_id=session_id)
        serializer = UserPreferenceSerializer(pref)
        return Response(serializer.data)

    def put(self, request):
        session_id = request.headers.get('X-Client-Session', 'default-user')
        pref, _ = UserPreference.objects.get_or_create(client_session_id=session_id)
        serializer = UserPreferenceSerializer(pref, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
