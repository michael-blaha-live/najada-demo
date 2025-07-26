import pytest
from rest_framework.test import APIClient
from api.eshop.models.ingredient import Ingredient
from api.eshop.serializers.ingredient import IngredientSerializer
from api.eshop.tests.factories import IngredientFactory


@pytest.mark.django_db
class TestGetIngredients:

    def test_get_ingredients_empty_list(self, api_client):
        """
        GIVEN no Ingredient instances exist in the database
        WHEN a GET request is made to /api/eshop/ingredients/
        THEN the API should return an empty list with 200 OK status.
        """
        response = api_client.get('/api/eshop/ingredients/')

        assert response.status_code == 200
        assert response.json() == []

    def test_get_ingredients_populated_list(self, api_client):
        """
        GIVEN multiple Ingredient instances exist in the database
        WHEN a GET request is made to /api/eshop/ingredients/
        THEN the API should return a list of serialized Ingredient objects with 200 OK status.
        """
        # Arrange: Create test data (some available, some not)
        ingredient1 = IngredientFactory(name="Šunka", _stored_qty=10)  # Should be available
        ingredient2 = IngredientFactory(name="Sýr Eidam", _stored_qty=0)  # Should be unavailable
        ingredient3 = IngredientFactory(name="Rajče", _stored_qty=5)  # Should be available
        
        # Act: Make the API request
        response = api_client.get('/api/eshop/ingredients/')

        # Assert: Check the response
        assert response.status_code == 200
        
        # Prepare expected data from created objects and sort for consistent comparison
        all_ingredients = [ingredient1, ingredient2, ingredient3]
        
        # We need to explicitly check the is_available status based on your model's logic
        # For the serializer, we expect 'ingredient_name' and 'is_available'
        expected_data_list = []
        for ing in all_ingredients:
            expected_data_list.append({
                'id': ing.id,
                'ingredient_name': ing.name,
                'is_available': ing.is_available  # This will come from the model's property/field
            })

        # Sort both lists by 'ingredient_name' for consistent comparison
        expected_data_list_sorted = sorted(expected_data_list, key=lambda item: item['ingredient_name'])
        response_data_sorted = sorted(response.json(), key=lambda item: item['ingredient_name'])
        
        assert response_data_sorted == expected_data_list_sorted
