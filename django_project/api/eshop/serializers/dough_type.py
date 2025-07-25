from rest_framework import serializers
from api.eshop.models.dough_type import DoughType

class DoughTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoughType
        fields = ['id', 'name', 'extra_price', 'is_available']
        read_only_fields = ['id']
