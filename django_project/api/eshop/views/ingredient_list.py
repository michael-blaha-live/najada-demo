from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from api.eshop.serializers.ingredient import IngredientSerializer
from api.eshop.services.ingredient import IngredientService


class IngredientListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        GET /api/v1/ingredients/
        Returns a list of all ingredients by delegating to IngredientService.
        """
        ingredients = IngredientService.get_all_ingredients()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
