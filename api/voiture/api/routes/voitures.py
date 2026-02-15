from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import VoitureSerializer

from api.models import Voiture



@api_view(['GET'])
def get_voitures(request):
    voitures = Voiture.objects.all()
    serializer = VoitureSerializer(voitures, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_voiture(request, garageId):
    voiture = Voiture.objects.filter(garage=garageId)
    if not voiture:
        return Response({"detail": "Not found."}, status=404)
    serializer = VoitureSerializer(voiture,many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_voiture(request):
    serializer = VoitureSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
