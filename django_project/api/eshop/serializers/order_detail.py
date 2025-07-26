from rest_framework import serializers
from api.eshop.models.order import Order
from api.eshop.serializers.order_item_detail import OrderItemDetailSerializer


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemDetailSerializer(many=True, read_only=True)
    payment_type = serializers.CharField(source='payment_type.name', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'total_price',
            'price_without_vat',
            'vat_amount',
            'payment_type',
            'created_at',
            'updated_at',
            'items'
        ]
        read_only_fields = fields
