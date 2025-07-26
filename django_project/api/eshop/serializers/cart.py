from rest_framework import serializers
from api.eshop.models.cart import Cart
from api.eshop.serializers.cart_item_detail import CartItemDetailSerializer


class CartSerializer(serializers.ModelSerializer):
    items = CartItemDetailSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    vat = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    wo_vat_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'total_price', 'vat', 'wo_vat_price', 'items']
        read_only_fields = ['id', 'total_price', 'vat', 'wo_vat_price', 'items']
