import pytest
from rest_framework.test import APIClient
from api.eshop.models import DoughType
from api.eshop.serializers import DoughTypeSerializer
# --- Fixtures (for test setup) ---
# This will go to conftest.py later for reusability, but for now, keep them here for clarity.

@pytest.fixture
def api_client():
    """
    Returns an APIClient instance for making HTTP requests in tests.
    """
    return APIClient()

@pytest.fixture
def create_dough_type(db): # 'db' fixture provided by pytest-django for database access
    """
    Fixture to create a DoughType instance for tests.
    """
    def _create_dough_type(name, extra_price=0, is_available=True):
        return DoughType.objects.create(
            name=name,
            extra_price=extra_price,
            is_available=is_available
        )
    return _create_dough_type

# --- Test Class for GET /dough-types ---

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

    def test_get_dough_types_populated_list(self, api_client, create_dough_type):
        """
        GIVEN multiple DoughType instances exist in the database
        WHEN a GET request is made to /dough-types
        THEN the API should return a list of serialized DoughType objects with 200 OK status.
        """
        # Arrange: Create test data using the fixture
        dough1 = create_dough_type("světlá", 0, True)
        dough2 = create_dough_type("celozrnná", 10, True)
        dough3 = create_dough_type("bezlepková", 12, False)

        # Act: Make the API request
        response = api_client.get('/api/eshop/dough-types/')

        # Assert: Check the response
        assert response.status_code == 200
        all_dough_types = [dough1, dough2, dough3]
        
        all_dough_types_sorted_by_name = sorted(all_dough_types, key=lambda dt: dt.name)
        expected_data = DoughTypeSerializer(all_dough_types_sorted_by_name, many=True).data
        response_data_sorted_by_name = sorted(response.json(), key=lambda item: item['name'])
        
        assert response_data_sorted_by_name == expected_data
