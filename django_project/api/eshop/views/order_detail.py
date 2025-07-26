from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.eshop.serializers.order_detail import OrderDetailSerializer
from api.eshop.services.order import OrderService


class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        """
        GET /api/eshop/orders/{pk}/
        Returns details of a specific order for the authenticated user.
        """
        order = OrderService.get_order_by_id(pk, request.user)
        if not order:
            return Response(
                {"detail": "Order not found or does not belong to the user."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
