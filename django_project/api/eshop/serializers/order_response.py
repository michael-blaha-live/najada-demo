from rest_framework import serializers
from api.eshop.models.order import Order


class OrderResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'status']
        read_only_fields = ['id', 'status']
