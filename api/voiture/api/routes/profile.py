from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import ProfileSerializer

from api.models import Profile



@api_view(['GET'])
def get_profile(request, userId):
    profile = Profile.objects.filter(user=userId)
    if not profile:
        return Response({"detail": "Not found."}, status=404)
    serializer = ProfileSerializer(profile,many=True)
    return Response(serializer.data)
