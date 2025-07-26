from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from api.eshop.serializers.dough_type import DoughTypeSerializer
from api.eshop.services.dough_type import DoughTypeService


class DoughTypeListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        GET /api/v1/dough-types/
        Returns a list of all dough types by delegating to DoughTypeService.
        """
        dough_types = DoughTypeService.get_all_dough_types()
        # Explicitly serialize the data retrieved from the service
        serializer = DoughTypeSerializer(dough_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
