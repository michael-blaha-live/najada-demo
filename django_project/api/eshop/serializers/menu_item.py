from rest_framework import serializers
from api.eshop.models.menu_item import MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    ingredients_ids = serializers.SerializerMethodField()
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'base_price', 'ingredients', 'ingredients_ids', 'is_available']
        read_only_fields = ['id', 'name', 'base_price', 'ingredients', 'ingredients_ids', 'is_available']

    def get_ingredients(self, obj):
        return [ingredient.name for ingredient in obj.ingredients.all()]

    def get_ingredients_ids(self, obj):
        return [ingredient.id for ingredient in obj.ingredients.all()]
