import pytest
from rest_framework.test import APIClient
from api.eshop.models import DoughType
from api.eshop.serializers import DoughTypeSerializer
from api.eshop.tests.factories import IngredientFactory, DoughTypeFactory, MenuItemFactory


@pytest.mark.django_db
class TestGetDoughTypes:

    def test_get_dough_types_empty_list(self, api_client):
        """
        GIVEN no DoughType instances exist in the database
        WHEN a GET request is made to /dough-types
        THEN the API should return an empty list with 200 OK status.
        """
        response = api_client.get('/api/eshop/dough-types/')

        assert response.status_code == 200
        assert response.json() == []

    def test_get_dough_types_populated_list(self, api_client):
        """
        GIVEN multiple DoughType instances exist in the database
        WHEN a GET request is made to /dough-types
        THEN the API should return a list of serialized DoughType objects with 200 OK status.
        """
        # Arrange: Create test data using the fixture
        dough1 = DoughTypeFactory(name="světlá", extra_price=0, is_available=True)
        dough2 = DoughTypeFactory(name="celozrnná", extra_price=10, is_available=True)
        dough3 = DoughTypeFactory(name="bezlepková", extra_price=12, is_available=False)

        # Act: Make the API request
        response = api_client.get('/api/eshop/dough-types/')

        # Assert: Check the response
        assert response.status_code == 200
        all_dough_types = [dough1, dough2, dough3]
        
        all_dough_types_sorted_by_name = sorted(all_dough_types, key=lambda dt: dt.name)
        expected_data = DoughTypeSerializer(all_dough_types_sorted_by_name, many=True).data
        response_data_sorted_by_name = sorted(response.json(), key=lambda item: item['name'])
        
        assert response_data_sorted_by_name == expected_data
