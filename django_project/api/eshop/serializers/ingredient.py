from rest_framework import serializers
from api.eshop.models.ingredient import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='name', read_only=True)
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = Ingredient
        fields = ['id', 'ingredient_name', 'is_available']
        read_only_fields = ['id', 'ingredient_name', 'is_available']
