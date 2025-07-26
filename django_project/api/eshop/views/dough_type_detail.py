from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from api.eshop.serializers.dough_type import DoughTypeSerializer
from api.eshop.services.dough_type import DoughTypeService


class DoughTypeDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk, *args, **kwargs):  # 'pk' will come from URLconf
        """
        GET /api/v1/dough-types/{pk}/
        Returns details of a specific dough type by delegating to DoughTypeService.
        """
        dough_type = DoughTypeService.get_dough_type_by_id(pk)
        if not dough_type:
            return Response(
                {"detail": "Dough type not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = DoughTypeSerializer(dough_type)
        return Response(serializer.data, status=status.HTTP_200_OK)
