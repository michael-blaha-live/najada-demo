from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class HeartbeatAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        GET /api/eshop/heartbeat
        Returns a list of all dough types by delegating to DoughTypeService.
        """
        return Response({'healthy': True}, status=status.HTTP_200_OK)
