from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.eshop.serializers.cart import CartSerializer
from api.eshop.serializers.cart_item_patch_request import CartItemPatchRequestSerializer
from api.eshop.services.cart import CartService


class CartItemDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, *args, **kwargs):
        serializer = CartItemPatchRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_quantity = serializer.validated_data['quantity']

        try:
            cart = CartService.update_cart_item_quantity(pk, new_quantity, request.user)
            response_serializer = CartSerializer(cart)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            if "not found" in str(e).lower():
                return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            CartService.remove_cart_item(pk, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            if "not found" in str(e).lower():
                return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
