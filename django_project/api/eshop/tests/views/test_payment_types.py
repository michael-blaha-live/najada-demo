import pytest
from rest_framework.test import APIClient
from api.eshop.models.payment_type import PaymentType
from api.eshop.serializers.payment_type import PaymentTypeSerializer
from api.eshop.tests.factories import PaymentTypeFactory


@pytest.mark.django_db
class TestGetPaymentTypes:

    def test_get_payment_types_empty_list(self, api_client):
        """
        GIVEN no PaymentType instances exist in the database
        WHEN a GET request is made to /api/eshop/payment-types/
        THEN the API should return an empty list with 200 OK status.
        """
        response = api_client.get('/api/eshop/payment-types/')

        assert response.status_code == 200
        assert response.json() == []

    def test_get_payment_types_populated_list(self, api_client):
        """
        GIVEN multiple PaymentType instances exist in the database
        WHEN a GET request is made to /api/v1/payment-types/
        THEN the API should return a list of serialized PaymentType objects with 200 OK status.
        """
        # Arrange: Create test data
        payment1 = PaymentTypeFactory(name="cash")
        payment2 = PaymentTypeFactory(name="credit card")
        
        # Act: Make the API request
        response = api_client.get('/api/eshop/payment-types/')

        # Assert: Check the response
        assert response.status_code == 200
        
        # Serialize the expected data from the created objects and sort for consistent comparison
        all_payment_types = [payment1, payment2]
        expected_data = PaymentTypeSerializer(sorted(all_payment_types, key=lambda pt: pt.name), many=True).data
        
        # Sort the actual response data for consistent comparison
        response_data_sorted = sorted(response.json(), key=lambda item: item['payment_type'])
        
        assert response_data_sorted == expected_data
