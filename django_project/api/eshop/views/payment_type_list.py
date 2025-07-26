from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from api.eshop.serializers.payment_type import PaymentTypeSerializer
from api.eshop.services.payment_type import PaymentTypeService  # Assuming you will create this service


class PaymentTypeListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        GET /api/v1/payment-types/
        Returns a list of all payment types by delegating to PaymentTypeService.
        """
        payment_types = PaymentTypeService.get_all_payment_types()
        serializer = PaymentTypeSerializer(payment_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
