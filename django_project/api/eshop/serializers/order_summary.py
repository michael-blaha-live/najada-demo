from rest_framework import serializers
from api.eshop.models.order import Order


class OrderSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'total_price', 'created_at']
        read_only_fields = fields
