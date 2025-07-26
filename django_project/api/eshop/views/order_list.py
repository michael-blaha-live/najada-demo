from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.eshop.serializers.order_summary import OrderSummarySerializer
from api.eshop.services.order import OrderService


class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        GET /api/eshop/orders/
        Returns a list of all orders for the authenticated user.
        """
        orders = OrderService.get_user_orders(request.user)
        serializer = OrderSummarySerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
