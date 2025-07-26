from rest_framework import serializers
from api.eshop.models.order_item import OrderItem


class OrderItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'menu_item_name_at_order',
            'dough_type_name_at_order',
            'quantity',
            'unit_price_at_order',
            'note'
        ]
        read_only_fields = fields
