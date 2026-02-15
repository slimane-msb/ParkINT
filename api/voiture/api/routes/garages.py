from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers import GarageSerializer

from api.models import Garage



@api_view(['GET'])
def get_garages(request):
    garages = Garage.objects.all()
    serializer = GarageSerializer(garages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_garage(request, pk):
    garage = get_object_or_404(Garage, pk=pk)
    serializer = GarageSerializer(garage)
    return Response(serializer.data)

@api_view(['POST'])
def add_garage(request):
    serializer = GarageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit_garage(request, pk):
    garage = get_object_or_404(Garage, pk=pk)
    serializer = GarageSerializer(garage, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_garage(request, pk):
    garage = get_object_or_404(Garage, pk=pk)
    garage.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
