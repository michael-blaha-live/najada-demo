from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.eshop.serializers.cart import CartSerializer
from api.eshop.serializers.cart_item_request import CartItemRequestSerializer
from api.eshop.services.cart import CartService


class CartItemAddAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CartItemRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            cart = CartService.add_item_to_cart(
                cart=CartService.get_or_create_cart_for_user(request.user),
                menu_item_id=serializer.validated_data['menu_item_id'],
                dough_type_id=serializer.validated_data['dough_type_id'],
                quantity=serializer.validated_data['quantity'],
                note=serializer.validated_data.get('note')
            )
            response_serializer = CartSerializer(cart)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
