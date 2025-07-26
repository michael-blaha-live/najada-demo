from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.eshop.services.order import OrderService
from api.eshop.serializers.order_create_request import OrderCreateRequestSerializer
from api.eshop.serializers.order_response import OrderResponseSerializer


class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = OrderCreateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_id = serializer.validated_data['cart_id']
        payment_type_id = serializer.validated_data['payment_type_id']

        try:
            order = OrderService.place_order(cart_id, payment_type_id, request.user)
            response_serializer = OrderResponseSerializer(order)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
