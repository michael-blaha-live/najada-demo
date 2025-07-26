from rest_framework import serializers


class CartItemPatchRequestSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0)  # Allow 0 to remove item
