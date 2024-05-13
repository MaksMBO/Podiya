from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from events.models import City
from events.serializers.cities import CitySerializer


class CityDetail(APIView):
    """
    Retrieve a city instance.
    """
    def get(self, request, pk):
        try:
            pk = int(pk)
        except ValueError:
            return Response({"error": "ID must be a valid integer."}, status=status.HTTP_400_BAD_REQUEST)

        city = get_object_or_404(City, pk=pk)
        serializer = CitySerializer(city)
        return Response(serializer.data)