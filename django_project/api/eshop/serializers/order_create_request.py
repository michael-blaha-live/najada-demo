from rest_framework import serializers
from api.eshop.models.order import Order
from api.eshop.serializers.order_item_detail import OrderItemDetailSerializer


class OrderCreateRequestSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    payment_type_id = serializers.IntegerField()
