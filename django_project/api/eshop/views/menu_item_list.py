from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from api.eshop.serializers.menu_item import MenuItemSerializer
from api.eshop.services.menu_item import MenuItemService


class MenuItemListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        GET /api/eshop/menu-items/
        Returns a list of all menu items.
        """
        menu_items = MenuItemService.get_all_menu_items()
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
