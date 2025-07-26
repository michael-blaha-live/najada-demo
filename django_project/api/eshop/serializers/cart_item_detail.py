from rest_framework import serializers
from api.eshop.models.cart_item import CartItem


class CartItemDetailSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    menu_item_id = serializers.IntegerField(source='menu_item.id', read_only=True)
    dough_type_id = serializers.IntegerField(source='dough_type.id', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'menu_item_id', 'dough_type_id', 'quantity', 'note', 'price']
        read_only_fields = ['id', 'menu_item_id', 'dough_type_id', 'quantity', 'note', 'price']
