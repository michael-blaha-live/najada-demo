from rest_framework import serializers
from api.eshop.models.payment_type import PaymentType


class PaymentTypeSerializer(serializers.ModelSerializer):
    payment_type = serializers.CharField(source='name', read_only=True)

    class Meta:
        model = PaymentType
        fields = ['id', 'payment_type']
        read_only_fields = ['id', 'payment_type']
