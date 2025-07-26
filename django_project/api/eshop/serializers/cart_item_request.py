from rest_framework import serializers
from api.eshop.models.cart_item import CartItem


class CartItemRequestSerializer(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
    dough_type_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    note = serializers.CharField(max_length=255, required=False, allow_blank=True)
