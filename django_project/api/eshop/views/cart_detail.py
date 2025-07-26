from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.eshop.serializers.cart import CartSerializer
from api.eshop.services.cart import CartService


class CartDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        GET /api/eshop/cart/
        Returns the current authenticated user's cart.
        """
        cart = CartService.get_or_create_cart_for_user(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
